"""
Client for the Vaarhaft FraudScanner API.

This module contains the client for interacting with the Vaarhaft FraudScanner API.
"""

import csv
import datetime
import os
import time
import uuid
import zipfile
from os import PathLike
from typing import List, Optional, Tuple, Union

import aiofiles

from vaarhaft.fraudscanner.request import FraudScannerRequest, RequestHeaders
from vaarhaft.fraudscanner.response.base import FraudScannerResponse


class FraudScannerClient:
    """Client for the FraudScanner API. Can be used as an async context manager."""

    def __init__(self, api_key: str, attachments_output_dir: str) -> None:
        """
        Initialize the client with an API key and an optional output directory.

        :param api_key: The API key for authenticating with the FraudScanner API.
        :param attachments_output_dir: Optional directory to save attachments to. If not provided, attachments will not be saved.
        """
        self.api_key = api_key
        self.output_dir = attachments_output_dir

    async def __aenter__(self) -> "FraudScannerClient":
        """
        Enter the async context manager. Creates the output directory if it doesn't exist.

        :returns: The client instance.
        """
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager."""
        pass

    async def send(
        self, 
        case_number: str, 
        file_path: Optional[Union[str, Union[str, PathLike]]],
        issue_date: Optional[str] = None,
        contact_email: Optional[str] = None
    ) -> FraudScannerResponse:
        """
        Send a request to the FraudScanner API.

        :param case_number: The case number for the request.
        :param file_path: Optional path to the file to be scanned. If not provided, no file will be sent.
        :param issue_date: Optional issue date for the request.
        :param contact_email: Optional contact email for the request.
        :returns: The response from the FraudScanner API.
        """
        headers = RequestHeaders(
            api_key=self.api_key,
            case_number=case_number,
            issue_date=issue_date,
            contact_email=contact_email
        )
        request = FraudScannerRequest(headers=headers, file_path=file_path, output_dir=self.output_dir)
        return await request.send()
    
    async def batched(self, *, case_number_base: str, input_dir: Union[str, PathLike], output_file: Union[str, PathLike] = None,
                      issue_date: Optional[str] = None, contact_email: Optional[str] = None) -> None:
        """
        Process multiple files in batches and send them to the FraudScanner API.
        Reads in files from the specified directory, processes them in batches, and saves the results to a CSV (output-)file.
        Useful for initially getting previous large amounts cases into the system in one go and without much setup.

        :param case_number_base: Base case number to use for all batches. Maximum 10 characters long.
        :param input_dir: Directory containing files to process
        :param output_file: Path to save CSV results (default: timestamped file in current directory)
        :param issue_date: Optional issue date to include with the request
        :param contact_email: Optional contact email to include with the request
        """
        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
            raise ValueError(f"Input directory '{input_dir}' does not exist or is not a directory.")
        if not case_number_base or len(case_number_base) > 10 or len(case_number_base) < 3:
            raise ValueError("Batch case number base must be between 3 and 10 characters long.")

        fieldnames = [
            "Case Number",
            "Filename",
            "Item ID",
            "Item Type",
            "Item Position",
            "Suspicion Level",
            "PDF file-level-analyses",
            "Image Quality",
            "Metadata",
            "C2PA",
            "Doublet Check",
            "Internet Reverse Search",
            "Tampered Detection",
            "Generated Detection",
        ]

        if not output_file:
            # Create default output file name based on current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            output_file = os.path.join(os.path.curdir, f"batch_results_{timestamp}.csv")

        with open(output_file, "w", newline='', encoding="utf-8") as f:
            # Initialize CSV
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            batch_number = 0
            batched_filenames = []
            processed_files = 0
            start_time = time.time()
            whole_batch_uuid = str(uuid.uuid4())

            all_files = os.listdir(input_dir)
            for filename in all_files:
                file_path = os.path.join(input_dir, filename)
                if not os.path.isfile(file_path) or not self._is_allowed_filename(filename):
                    print(f"\nSkipping unprocessable file: '{filename}'")
                    continue

                batched_filenames.append(filename)

                if len(batched_filenames) < 5:
                    continue
                files_processed, batch_number = await self._process_batch(
                    batched_filenames=batched_filenames,
                    input_dir=input_dir,
                    batch_number=batch_number,
                    whole_batch_uuid=whole_batch_uuid,
                    case_number_base=case_number_base,
                    issue_date=issue_date,
                    contact_email=contact_email,
                    writer=writer,
                    is_final_batch=False
                )

                processed_files += files_processed
                batched_filenames = []  # Reset for the next batch

            # Process remaining files
            if batched_filenames:
                files_processed, _ = await self._process_batch(
                    batched_filenames=batched_filenames,
                    input_dir=input_dir,
                    batch_number=batch_number,
                    whole_batch_uuid=whole_batch_uuid,
                    case_number_base=case_number_base,
                    issue_date=issue_date,
                    contact_email=contact_email,
                    writer=writer,
                    is_final_batch=True
                )
                processed_files += files_processed

        batch_duration = time.time() - start_time
        self._sort_csv(output_file)
        print(f"\n\n--- Done processing {processed_files} files from {input_dir} after {batch_duration:.1f} seconds.\n"
              f"Saved results to {output_file}\n")

    async def _process_batch(self, batched_filenames: List[str], input_dir: Union[str, PathLike], batch_number: int,
                      whole_batch_uuid: str, case_number_base: str, issue_date: Optional[str],
                      contact_email: Optional[str], writer: csv.DictWriter, is_final_batch: bool = False) -> Tuple[int, int]:
        """
        Process a batch of files.

        :param batched_filenames: List of filenames to process in the batch.
        :param input_dir: Directory where the files are located.
        :param batch_number: Current batch number.
        :param whole_batch_uuid: UUID for the entire batch.
        :param case_number_base: Base case number for the batch.
        :param issue_date: Issue date for the batch.
        :param contact_email: Contact email for the batch.
        :param writer: CSV writer to write the results.
        :param is_final_batch: Boolean indicating if this is the final batch.
        :return: Number of files processed and the updated batch number.
        """
        zip_file_path = ""
        try:
            # Process the batch of files
            batch_type = "final batch" if is_final_batch else "batch"
            print(f"\nProcessing {batch_type} of files: {batched_filenames}")

            # Create zip file for the batch request
            zip_filename = f"batch_{batch_number}__{whole_batch_uuid}.zip"  # Unique filename for the zip in case of parallel batch processing
            zip_file_path = os.path.join(input_dir, zip_filename)

            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file in batched_filenames:
                    file_path = os.path.join(input_dir, file)
                    # Read file content asynchronously
                    async with aiofiles.open(file_path, "rb") as f:
                        content = await f.read()
                        # Add the file to the zip archive with its original name
                        zip_file.writestr(file, content)

            case_number = f"__INVENTORY-BATCH__ {case_number_base} [{batch_number}]"
            batch_number += 1

            # Create a request for the batch
            response = await self.send(
                case_number=case_number,
                file_path=zip_file_path,
                issue_date=issue_date,
                contact_email=contact_email
            )

            for item_id_tup, result_item in response.get_all_items():
                row = {
                    "Case Number": response.caseNumber,
                    "Filename": item_id_tup.file_name,
                    "Item ID": item_id_tup.item_uuid,
                    "Item Type": result_item.item_type,
                    "Item Position": result_item.position,
                    "Suspicion Level": result_item.suspicion_level,
                    "Tampered Detection": result_item.analyses.tamperedDetection,
                }
                # Add image-specific analysis fields if the item type is IMAGE
                if result_item.item_type == "image":
                    row.update({
                        "Image Quality": result_item.analyses.imageQuality,
                        "Metadata": result_item.analyses.metadata,
                        "C2PA": result_item.analyses.c2pa,
                        "Doublet Check": result_item.analyses.doubletCheck,
                        "Internet Reverse Search": result_item.analyses.reverseSearch,
                        "Generated Detection": result_item.analyses.generatedDetection,
                    })
                # Add the row to the CSV file
                writer.writerow(row)

            # Create dummy items for files to insert file-level analyses
            for result_filename, result_file in response.Files:
                if not result_file.file_level_analyses or not any(analysis for analysis in result_file.file_level_analyses.__dict__.values()):
                    continue
                row = {
                    "Case Number": response.caseNumber,
                    "Filename": result_filename,
                    "Item ID": None,
                    "Item Type": "file-level-analyses-dummy",
                    "Item Position": None,
                    "Suspicion Level": result_file.suspicion_level,
                    "PDF file-level-analyses": result_file.file_level_analyses.pdf_analyses,
                }
                # Add the row to the CSV file
                writer.writerow(row)

            print(f"\tProcessed files: {batched_filenames}")
            return len(batched_filenames), batch_number

        except Exception as e:
            print(f"\tError processing batched files: {batched_filenames}:\n\t{e}")
            return 0, batch_number
        finally:
            if zip_file_path and os.path.exists(zip_file_path):
                os.remove(zip_file_path)
            else:
                print(f"\tError: Zip file {zip_file_path} does not exist or could not be removed.")


    @staticmethod
    def _is_allowed_filename(filename: str) -> bool:
        """Check if the filename is allowed based on its extension."""
        allowed_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".heic", ".webp", ".pdf"}
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)

    @staticmethod
    def _sort_csv(csv_file: Union[str, PathLike]) -> None:
        """
        Sort the rows of a CSV file by Filename, Item Position, and Item Type.

        :param csv_file: Path to the CSV file to sort
        """
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            def sort_key(row):
                filename = row.get('Filename', '')
                pos_str = row.get('Item Position', '')
                try:
                    position = int(pos_str) if pos_str and pos_str.strip() else -1
                except (ValueError, TypeError):
                    position = -1
                item_type = row.get('Item Type', '')
                return filename or '', position, item_type or ''

            sorted_rows = sorted(rows, key=sort_key)
            if sorted_rows:
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(sorted_rows)
        except Exception as e:
            print(f"Error sorting CSV file {csv_file}: {e}")

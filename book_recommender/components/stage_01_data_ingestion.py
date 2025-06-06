import os
import sys
import kagglehub
import zipfile
from typing import Optional

from book_recommender.exception.exception_handler import AppException
from book_recommender.logger import log
from book_recommender.configuration.config import AppConfig


class DataIngestion:
    def __init__(self, app_config: Optional[AppConfig] = None):
        """
        Initialize Data Ingestion
        """
        try:
            log.info(f"{'-'*20} Data Ingestion Initiated {'-'*20}")
            if app_config is None:
                app_config = AppConfig()
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    def download_data(self) -> str:
        """
        Fetch data from Kaggle.
        
        Returns:
            str: Path to downloaded zip file
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir, exist_ok=True)

            file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(raw_data_dir, file_name)

            log.info(f"Downloading data from: {dataset_url} to {zip_file_path}")
            kagglehub.dataset_download(dataset_url, path=zip_file_path)
            log.info(f"Download complete: {zip_file_path}")

            return zip_file_path
        except Exception as e:
            raise AppException(e, sys) from e
        
    def extract_zip_file(self, zip_file_path: str) -> None:
        """
        Extract the downloaded zip file to the ingestion directory.
        
        Args:
            zip_file_path (str): Path to the downloaded zip file
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(ingested_dir)

            log.info(f"Extracted: {zip_file_path} to {ingested_dir}")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_ingestion(self) -> None:
        """
        Orchestrate the full data ingestion process.
        """
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path)
            log.info("Data ingestion completed successfully.")
        except Exception as e:
            raise AppException(e, sys) from e

import os
import subprocess
from dotenv import load_dotenv
import sys
import kagglehub
from six.moves import urllib
import zipfile
from typing import Optional
from book_recommender.constants import GENRE_FILE_NAME
from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig


class DataIngestion:
    def __init__(self, app_config: Optional[AppConfig] = None):
        """
        Initialize Data Ingestion
        """
        try:
            logging.info(f"{'-'*20} Data Ingestion Initiated {'-'*20}")
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
            load_dotenv()
            dataset_slug = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)

            book_file_name =  dataset_slug.split("/")[-1]
            zip_file_path = os.path.join(zip_download_dir, f"{book_file_name}.zip")

            logging.info(f"Downloading data from: {dataset_slug} to {zip_file_path}")
            #kagglehub.dataset_download(dataset_url, path=zip_file_path)
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset_slug, "-p", zip_download_dir, "--force"], check=True)
            logging.info(f"Zipped Dataset Downloaded to: {zip_file_path}")


            ingested_dir = os.makedirs(self.data_ingestion_config.ingested_dir, exist_ok=True)
            genre_file_path = os.path.join(ingested_dir, GENRE_FILE_NAME)
            urllib.request.urlretrieve(dataset_slug, genre_file_path)
            logging.info(f"Genre file downloaded to: {genre_file_path}")
            
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

            logging.info(f"Extracted: {zip_file_path} to {ingested_dir}")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def initiate_data_ingestion(self) -> None:
        """
        Orchestrate the full data ingestion process.
        """
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path)
            logging.info("Data ingestion completed successfully.")
        except Exception as e:
            raise AppException(e, sys) from e

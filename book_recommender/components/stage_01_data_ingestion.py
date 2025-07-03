import os
import subprocess
from dotenv import load_dotenv
import sys
from six.moves import urllib
import zipfile
from typing import Optional
from book_recommender.constants import GENRE_FILE_NAME
from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json


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
        

    def _load_kaggle_credentials_from_aws(self):
        """
        Try to fetch Kaggle credentials from AWS Secrets Manager.
        Return dict with keys 'KAGGLE_USERNAME' and 'KAGGLE_KEY' or None if fails.
        """
        secret_name = os.getenv("KAGGLE_SECRET_NAME")  # Set this env var in Docker or EC2
        region_name = os.getenv("AWS_REGION", "us-east-1")

        if not secret_name:
            logging.warning("KAGGLE_SECRET_NAME env var not set, skipping AWS Secrets Manager.")
            return None

        try:
            client = boto3.client('secretsmanager', region_name=region_name)
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)

            secret_string = get_secret_value_response.get('SecretString')
            if secret_string:
                secret = json.loads(secret_string)
                # Expect secret dict like: {"KAGGLE_USERNAME": "...", "KAGGLE_KEY": "..."}
                if 'KAGGLE_USERNAME' in secret and 'KAGGLE_KEY' in secret:
                    return secret
            logging.warning("Secret fetched but missing KAGGLE_USERNAME or KAGGLE_KEY.")
        except (BotoCoreError, ClientError) as e:
            logging.warning(f"Could not fetch secret from AWS Secrets Manager: {e}")
        except Exception as e:
            logging.warning(f"Unexpected error accessing AWS Secrets Manager: {e}")
        return None
    
    def download_data(self) -> str:
        """
        Fetch data from Kaggle.
        Returns:
            str: Path to downloaded zip file
        """
        try:
            # Try AWS Secrets Manager first
            creds = self._load_kaggle_credentials_from_aws()

            if creds is None:
                # fallback to .env locally
                load_dotenv()
                creds = {
                    "KAGGLE_USERNAME": os.getenv("KAGGLE_USERNAME"),
                    "KAGGLE_KEY": os.getenv("KAGGLE_KEY")
                }
            os.environ["KAGGLE_USERNAME"] = creds["KAGGLE_USERNAME"]
            os.environ["KAGGLE_KEY"] = creds["KAGGLE_KEY"]
            
            dataset_slug = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)

            book_file_name =  dataset_slug.split("/")[-1]
            zip_file_path = os.path.join(zip_download_dir, f"{book_file_name}.zip")

            logging.info(f"Downloading data from: {dataset_slug} to {zip_file_path}")
            
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset_slug, "-p", zip_download_dir, "--force"], check=True)
            logging.info(f"Zipped Dataset Downloaded to: {zip_file_path}")

            # Ensure directory exists
            os.makedirs(self.data_ingestion_config.ingested_dir, exist_ok=True)
            genre_url = self.data_ingestion_config.genre_url
            # Define the download path
            genre_file_path = os.path.join(self.data_ingestion_config.ingested_dir, GENRE_FILE_NAME)
            # Download the file from the web to the local path
            urllib.request.urlretrieve(genre_url, genre_file_path)

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

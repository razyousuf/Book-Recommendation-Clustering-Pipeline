import os
import sys

from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.log import logging
from book_recommender.utils.util import read_yaml_file
from book_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig
from book_recommender.constants import *


class AppConfig:

    def __init__(self, config_file_path:str = CONFIG_FILE_PATH):
        try:
            self.config = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config = self.config['data_ingestion_config']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(dataset_download_url=data_ingestion_config['dataset_download_url'],
                                           ingested_dir=ingested_data_dir,
                                           raw_data_dir=raw_data_dir)
            logging.info(f"Data Ingestion Config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config = self.config['data_validation_config']
            data_ingestion_config = self.config['data_ingestion_config']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']
            book_csv_file = data_validation_config['book_csv_file']
            rating_csv_file = data_validation_config['rating_csv_file']

            book_csv_file_path = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], book_csv_file)
            book_rating_csv_file_path = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], rating_csv_file)
            cleaned_data_dir = os.path.join(artifacts_dir, dataset_dir, data_validation_config['cleaned_data_dir'])
            serialized_object_dir = os.path.join(artifacts_dir, dataset_dir, data_validation_config['serialized_object_dir'])

            response = DataValidationConfig(
                                            book_csv_file=book_csv_file_path,
                                            rating_csv_file=book_rating_csv_file_path,
                                            cleaned_data_dir=cleaned_data_dir,
                                            serialized_object_dir=serialized_object_dir)
            logging.info(f"Data Validation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
        
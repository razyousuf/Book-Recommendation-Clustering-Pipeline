import os
import sys

from book_recommender.exception.exception_handler import AppException
from book_recommender.logger import log
from book_recommender.utils.util import read_yaml_file
from book_recommender.entity.config_entity import DataIngestionConfig
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
            log.info(f"Data Ingestion Config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
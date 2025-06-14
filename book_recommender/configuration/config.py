import os
import sys

from book_recommender.exception.exception_handler import AppException
from book_recommender.logger.log import logging
from book_recommender.utils.util import read_yaml_file
from book_recommender.entity.config_entity import (
                                                    DataIngestionConfig, 
                                                    DataValidationConfig, 
                                                    DataTransformationConfig,
                                                    ModelTrainerConfig,
                                                    ModelRecommendationConfig
                                                    )
from book_recommender.constants import *


class AppConfig:
    """
    This class is responsible for reading the configuration file and providing access to various configuration settings.
    It reads the YAML configuration file and provides methods to access different configuration entities such as DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, and ModelRecommendationConfig.

    Attributes:
        config (dict): A dictionary containing the configuration settings read from the YAML file.
"""
    def __init__(self, config_file_path:str = CONFIG_FILE_PATH):
        try:
            self.config = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Reads the data ingestion configuration from the YAML file and returns a DataIngestionConfig object.

        Returns:
            DataIngestionConfig: An object containing the data ingestion configuration settings.
        """
        try:
            data_ingestion_config = self.config['data_ingestion_config']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(dataset_download_url=data_ingestion_config['dataset_download_url'],
                                           ingested_dir=ingested_data_dir,
                                           raw_data_dir=raw_data_dir,
                                           genre_url=data_ingestion_config['genre_dataset_url'])
                                           
            logging.info(f"Data Ingestion Config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Reads the data validation configuration from the YAML file and returns a DataValidationConfig object.
        
        Returns:
            DataValidationConfig: An object containing the data validation configuration settings.
        """
        try:
            data_validation_config = self.config['data_validation_config']
            data_ingestion_config = self.config['data_ingestion_config']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']
            book_csv_file = data_validation_config['book_csv_file']
            rating_csv_file = data_validation_config['rating_csv_file']
            genre_csv_file = data_validation_config['genre_csv_file']

            book_csv_file_path = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], book_csv_file)
            book_rating_csv_file_path = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], rating_csv_file)
            cleaned_data_dir = os.path.join(artifacts_dir, dataset_dir, data_validation_config['cleaned_data_dir'])
            serialized_object_dir = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'])
            genre_csv_file_path = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], genre_csv_file)

            response = DataValidationConfig(
                                            book_csv_file=book_csv_file_path,
                                            rating_csv_file=book_rating_csv_file_path,
                                            cleaned_data_dir=cleaned_data_dir,
                                            serialized_object_dir=serialized_object_dir,
                                            genre_csv_file=genre_csv_file_path
                                            )
            logging.info(f"Data Validation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Reads the data transformation configuration from the YAML file and returns a DataTransformationConfig object.
        
        Returns:
            DataTransformationConfig: An object containing the data transformation configuration settings.
        """
        try:
            data_transformation_config = self.config['data_transformation_config']
            data_validation_config = self.config['data_validation_config']
            data_ingestion_config = self.config['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
          
            clean_data_file_path = os.path.join(artifacts_dir, dataset_dir, data_validation_config['cleaned_data_dir'], CLEANED_DATA_FILENAME)
            transformed_data_dir = os.path.join(artifacts_dir, dataset_dir, data_transformation_config['transformed_data_dir'])

            response = DataTransformationConfig(
                clean_data_file_path=clean_data_file_path,
                transformed_data_dir=transformed_data_dir
            )

            logging.info(f"Data Transformation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Reads the model trainer configuration from the YAML file and returns a ModelTrainerConfig object.
        
        Returns:
            ModelTrainerConfig: An object containing the model trainer configuration settings.
        """
        try:
            model_trainer_config = self.config['model_trainer_config']
            data_transformation_config = self.config['data_transformation_config']
            data_ingestion_config = self.config['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']

            transformed_data_file_path = os.path.join(artifacts_dir, dataset_dir, data_transformation_config['transformed_data_dir'], TRANSFORMED_DATA_FILENAME)
            trained_model_dir = os.path.join(artifacts_dir, model_trainer_config['trained_model_dir'])
            trained_model_name = model_trainer_config['trained_model_name']

            response = ModelTrainerConfig(
                transformed_data_file_path=transformed_data_file_path,
                trained_model_dir=trained_model_dir,
                trained_model_name=trained_model_name
            )

            logging.info(f"Model Trainer Config: {response}")
            return response
        
        except Exception as e:
            raise AppException(e, sys) from e
        

    def get_recommendation_config(self) -> ModelRecommendationConfig:
        """
        Reads the recommendation configuration from the YAML file and returns a ModelRecommendationConfig object.
        
        Returns:
            ModelRecommendationConfig: An object containing the recommendation configuration settings.
        """
        try:
            recommendation_config = self.config['recommendation_config']
            model_trainer_config = self.config['model_trainer_config']
            data_validation_config = self.config['data_validation_config']
            trained_model_name = model_trainer_config['trained_model_name']
            artifacts_dir = self.config['artifacts_config']['artifacts_dir']
            trained_model_dir = os.path.join(artifacts_dir, model_trainer_config['trained_model_dir'])
            poster_api = recommendation_config['poster_api_url']
            

            book_name_serialized_objects = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'], BOOK_NAMES_FILENAME)
            book_pivot_serialized_objects = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'], BOOK_PIVOT_FILENAME)
            final_rating_serialized_objects = os.path.join(artifacts_dir, data_validation_config['serialized_objects_dir'], FINAL_RATINGS_FILENAME)

            trained_model_path = os.path.join(trained_model_dir,trained_model_name)
          
            response = ModelRecommendationConfig(
                book_name_serialized_objects = book_name_serialized_objects,
                book_pivot_serialized_objects = book_pivot_serialized_objects,
                final_rating_serialized_objects = final_rating_serialized_objects,
                trained_model_path = trained_model_path
            )

            logging.info(f"Model Recommendation Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
import os
import sys
import pickle
import pandas as pd
from book_recommender.constants import *
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException



class DataTransformation:
    """
    This class is responsible for transforming the data. It reads the clean data file, creates a pivot table of books and user ratings, and saves the pivot table to a file. It also saves the book names and the pivot table to be used in the web app.
    """
    def __init__(self, app_config = AppConfig()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformer(self):
        """
        Reads the clean data file, creates a pivot table of books and user ratings, and saves the pivot table to a file.
        Returns: None
        """
        try:
            df = pd.read_csv(self.data_transformation_config.clean_data_file_path)
            # Lets create a pivot table
            book_pivot = df.pivot_table(columns='user_id', index='title', values= 'rating')
            logging.info(f" Shape of book pivot table: {book_pivot.shape}")
            book_pivot.fillna(0, inplace=True)

            #saving pivot table data
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            pickle.dump(book_pivot,open(os.path.join(self.data_transformation_config.transformed_data_dir, TRANSFORMED_DATA_FILENAME),'wb'))
            logging.info(f"Saved pivot table data to {self.data_transformation_config.transformed_data_dir}")

            #keeping books name
            book_names = book_pivot.index

            #saving book_names objects for web app
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(book_names,open(os.path.join(self.data_validation_config.serialized_object_dir, BOOK_NAMES_FILENAME),'wb'))
            logging.info(f"Saved book_names serialization object to {self.data_validation_config.serialized_object_dir}")

            #saving book_pivot objects for web app (this is used for recommendation)
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(book_pivot,open(os.path.join(self.data_validation_config.serialized_object_dir, BOOK_PIVOT_FILENAME),'wb'))
            logging.info(f"Saved book_pivot serialization object to {self.data_validation_config.serialized_object_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_transformation(self):
        """
        Initiates the data transformation process by calling the get_data_transformer method. It logs the start and completion of the data transformation process.
        Returns: None
        """
        try:
            logging.info(f"{'+'*5}Data Transformation log started.{'+'*5} ")
            self.get_data_transformer()
            logging.info(f"{'+'*5}Data Transformation log completed.{'+'*5} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e



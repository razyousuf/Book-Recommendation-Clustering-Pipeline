import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException

class ModelTrainer:
    def __init__(self, app_config = AppConfig()):
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def train_model(self):
        try:
            # Load the pivot table data
            book_pivot = pickle.load(open(self.model_trainer_config.transformed_data_file_path, 'rb'))
            book_sparse = csr_matrix(book_pivot)

            model = NearestNeighbors(algorithm='brute')
            model.fit(book_sparse)

            # Save the trained model
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            model_file_name = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name)
            pickle.dump(model, open(model_file_name, 'wb'))
            logging.info(f"Trained model saved at: {model_file_name}")
        except Exception as e:
            raise AppException(e, sys) from e
        

    def initiate_model_training(self):
        try:
            logging.info(f"{'-'*20}Model Training log started.{'-'*20} ")
            self.train_model()
            logging.info(f"{'-'*20}Model Training log completed.{'-'*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
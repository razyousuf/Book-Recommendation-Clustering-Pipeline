import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException

class ModelTrainer:
    """
    This class is responsible for training the model. It loads the pivot table data, trains a NearestNeighbors model, and saves the trained model to a file.
    """
    def __init__(self, app_config = AppConfig()):
        """
        Initializes the ModelTrainer class with the model trainer configuration.

        Args:
            app_config (AppConfig): An instance of the AppConfig class to fetch configuration settings.
            """
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def train_model(self):
        """
        Trains the NearestNeighbors model using the pivot table data. It also saves the trained model to a specified directory.

        Returns: None
        """
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
        """
        Initiates the model training process by calling the train_model method. It logs the start and completion of the model training process.
        Args:
            self: The instance of the ModelTrainer class.
        Returns: None
        """
        try:
            logging.info(f"{'+'*5}Model Training log started.{'+'*5} \n\n")
            self.train_model()
            logging.info(f"{'+'*5}Model Training log completed.{'+'*5} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e
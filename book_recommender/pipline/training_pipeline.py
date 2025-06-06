from book_recommender.components.stage_01_data_ingestion import DataIngestion
#from book_recommender.components.data_transformation import DataTransformation
#from book_recommender.components.model_trainer import ModelTrainer


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        #self.data_transformation = DataTransformation()
        #self.model_trainer = ModelTrainer()

    def start_training_pipeline(self):
        """
        Starts the training pipeline
        """
        self.data_ingestion.initiate_data_ingestion()

    # def start_data_transformation(self):
    #     self.data_transformation.initiate_data_transformation()

    # def start_model_trainer(self):
    #     self.model_trainer.initiate_model_trainer()
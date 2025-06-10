from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["dataset_download_url",
                                                   "genre_url",
                                                   "raw_data_dir",
                                                   "ingested_dir"])


DataValidationConfig = namedtuple("DataValidationConfig", ["cleaned_data_dir",
                                                          "serialized_object_dir",
                                                          "book_csv_file",
                                                          "rating_csv_file",
                                                          "genre_csv_file"]
                                                          )

DataTransformationConfig = namedtuple("DataTransformationConfig", ["clean_data_file_path",
                                                                   "transformed_data_dir"])


ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["transformed_data_file_path",
                                                      "trained_model_dir",
                                                      "trained_model_name"])

ModelRecommendationConfig = namedtuple("ModelRecommendationConfig", ["book_name_serialized_objects",
                                                      "book_pivot_serialized_objects",
                                                      "final_rating_serialized_objects",
                                                      "trained_model_path"])

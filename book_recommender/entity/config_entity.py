from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["dataset_download_url",
                                                   "raw_data_dir",
                                                   "ingested_dir"])


DataValidationConfig = namedtuple("DataValidationConfig", ["cleaned_data_dir",
                                                          "serialized_object_dir",
                                                          "book_csv_file",
                                                          "rating_csv_file"])
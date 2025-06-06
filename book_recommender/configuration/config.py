import os
import sys

from book_recommender.exception.exception_handler import AppException
from book_recommender.logger import log
from book_recommender.entity.utils.util import read_yaml_file
from book_recommender.entity.config_entity import DataIngestionConfig
from book_recommender.constants import *


class AppConfig:

    def __init__(self, config_file_path:str = CONFIG_FILE_PATH):
        try:
            self.config = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys)

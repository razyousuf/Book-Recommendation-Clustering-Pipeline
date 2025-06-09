import os

ROOT_DIR = os.getcwd()
# Main config file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_FOLDER_NAME,CONFIG_FILE_NAME)

GENRE_FILE_NAME = "genre.csv"
USER_RATED_THRESHOLD = 150
BOOKS_RATED_THRESHOLD = 30
CLEANED_DATA_FILENAME = "cleaned_data.csv"
FINAL_RATINGS_FILENAME = "final_ratings.pkl"
BOOK_NAMES_FILENAME = "book_names.pkl"
BOOK_PIVOT_FILENAME = "book_pivot.pkl"
TRANSFORMED_DATA_FILENAME = "transformed_data.pkl"
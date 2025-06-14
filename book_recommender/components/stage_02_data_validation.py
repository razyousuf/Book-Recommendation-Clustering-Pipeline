import os
import sys
import ast 
import pandas as pd
import pickle
from book_recommender.logger.log import logging
from book_recommender.constants import *
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException
from book_recommender.utils.enrich_metadata import fetch_genre



class DataValidation:
    """
    This class is responsible for validating the data. It reads the ratings, books, and genre CSV files, cleans the data, and saves the cleaned data to a new CSV file. It also serializes the final ratings object for use in the web app.
    """
    def __init__(self, app_config = AppConfig()):
        try:
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    def preprocess_data(self):
        """
        This function preprocesses the data by reading the ratings, books, and genre CSV files, cleaning the data, and saving the cleaned data to a new CSV file. It also serializes the final ratings object for use in the web app.
        Returns: None
        Args:
            self: The instance of the DataValidation class.
        """
        try:
            ratings = pd.read_csv(self.data_validation_config.rating_csv_file, sep=";", encoding='latin-1', on_bad_lines='skip', low_memory=False)
            books = pd.read_csv(self.data_validation_config.book_csv_file, sep=";", encoding='latin-1', on_bad_lines='skip', low_memory=False)
            genre = pd.read_csv(self.data_validation_config.genre_csv_file, sep=",", encoding='latin-1', on_bad_lines='skip', low_memory=False)

            
            logging.info(f" Shape of ratings data file: {ratings.shape}")
            logging.info(f" Shape of books data file: {books.shape}")
            logging.info(f" Shape of genre data file: {genre.shape}")

            #Here Image URL columns is important for the poster. So, we will keep it
            books = books[['ISBN','Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher','Image-URL-L']]
            # Lets remane some wierd column names in books
            books =books.rename(columns=
                                {"Book-Title":'title',
                                'Book-Author':'author',
                                "Year-Of-Publication":'year',
                                "Publisher":"publisher",
                                "Image-URL-L":"image_url"
                            })

            # Extract the ISBN and genre from the genre dataset
            genre = genre[['ISBN', 'genre']]
            genre = genre.drop_duplicates(subset='ISBN')
            # Lets join genre with books
            books = books.merge(genre, on='ISBN', how='left') # left join, ensure all books are included
            logging.info(f" Shape of books data after merging with genre: {books.shape} \n {books.head()}")

            # Lets remane some wierd columns name in ratings
            ratings =ratings.rename(columns={
                                "User-ID":'user_id',
                                'Book-Rating':'rating'
                            })

            # Lets store users who had at least rated more than user_rated_threshold e.g. 200 books
            x = ratings['user_id'].value_counts() > USER_RATED_THRESHOLD
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]
            logging.info(f" Users with more than {USER_RATED_THRESHOLD} ratings: {ratings.head()} \n\n")
            # Now join ratings with books
            ratings_with_books = ratings.merge(books, on='ISBN')
            number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='title')

            # Lets take those books which got at least the defined threshold user ratings
            final_rating = final_rating[final_rating['num_of_rating'] >= BOOKS_RATED_THRESHOLD]
            
            # Now lets calculate average rating for each book
            final_rating['avg_rating'] = final_rating.groupby('ISBN')['rating'].transform('mean').round(3)

            # Now let's apply IMDb weighted rating formula to calculate the average rating for each book
            C = final_rating['avg_rating'].mean()
            m = final_rating['num_of_rating'].quantile(0.5)

            def weighted_rating(x, m=m, C=C):
                v = x['num_of_rating']
                R = x['avg_rating']
                return (v / (v + m)) * R + (m / (v + m)) * C
            
            final_rating['avg_rating'] = final_rating.apply(weighted_rating, axis=1).round(2)


            final_rating = final_rating.drop_duplicates(subset=["user_id", "ISBN"])

            # lets drop the duplicates
            logging.info(f" Shape of the final clean dataset:\n {final_rating.shape} \n and null check\n {final_rating.isnull().sum()} \n and head is\n {final_rating.head()}\n")
                        
            # Saving the cleaned data for transformation
            os.makedirs(self.data_validation_config.cleaned_data_dir, exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.cleaned_data_dir,CLEANED_DATA_FILENAME), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.cleaned_data_dir}")

            #saving final_rating objects for web app
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_object_dir, FINAL_RATINGS_FILENAME),'wb'))
            logging.info(f"Saved final_rating serialization object to:\n {self.data_validation_config.serialized_object_dir}")

        except Exception as e:
            logging.error("Data validation failed", exc_info=True)
            raise AppException(e, sys) from e

    
    def initiate_data_validation(self):
        """
        Initiates the data validation process by calling the preprocess_data method. It logs the start and completion of the data validation process.
        """
        try:
            logging.info(f"{'+'*5}Data Validation log started.{'+'*5} ")
            self.preprocess_data()
            logging.info(f"{'+'*5}Data Validation log completed.{'+'*5} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e



    
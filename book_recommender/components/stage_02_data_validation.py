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
    def __init__(self, app_config = AppConfig()):
        try:
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e


    
    def preprocess_data(self):
        try:
            ratings = pd.read_csv(self.data_validation_config.rating_csv_file, sep=";", encoding='latin-1', on_bad_lines='skip', low_memory=False)
            books = pd.read_csv(self.data_validation_config.book_csv_file, sep=";", encoding='latin-1', on_bad_lines='skip', low_memory=False)

            
            logging.info(f" Shape of ratings data file: {ratings.shape}")
            logging.info(f" Shape of books data file: {books.shape}")

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

            
            # Lets remane some wierd columns name in ratings
            ratings =ratings.rename(columns={
                                "User-ID":'user_id',
                                'Book-Rating':'rating'
                            })

            # Lets store users who had at least rated more than 200 books
            x = ratings['user_id'].value_counts() > USER_RATED_THRESHOLD
            y = x[x].index
            ratings = ratings[ratings['user_id'].isin(y)]

            # Now join ratings with books
            ratings_with_books = ratings.merge(books, on='ISBN')
            number_rating = ratings_with_books.groupby('title')['rating'].count().reset_index()
            number_rating.rename(columns={'rating':'num_of_rating'},inplace=True)
            final_rating = ratings_with_books.merge(number_rating, on='title')

            # Lets take those books which got at least 50 user ratings
            final_rating = final_rating[final_rating['num_of_rating'] >= BOOKS_RATED_THRESHOLD]

            # lets drop the duplicates
            final_rating.drop_duplicates(['user_id','title'],inplace=True)
            logging.info(f" Shape of the final clean dataset: {final_rating.shape}")
                        
            # Saving the cleaned data for transformation
            os.makedirs(self.data_validation_config.cleaned_data_dir, exist_ok=True)
            final_rating.to_csv(os.path.join(self.data_validation_config.cleaned_data_dir,CLEANED_DATA_FILENAME), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.cleaned_data_dir}")


            #saving final_rating objects for web app
            final_rating['genre'] = final_rating.apply(lambda row: fetch_genre(row['title'], row.get('author')), axis=1)
            os.makedirs(self.data_validation_config.serialized_object_dir, exist_ok=True)
            pickle.dump(final_rating,open(os.path.join(self.data_validation_config.serialized_object_dir, FINAL_RATINGS_FILENAME),'wb'))
            logging.info(f"Saved final_rating serialization object to {self.data_validation_config.serialized_object_dir}")

        except Exception as e:
            raise AppException(e, sys) from e

    
    def initiate_data_validation(self):
        try:
            logging.info(f"{'-'*20}Data Validation log started.{'-'*20} ")
            self.preprocess_data()
            logging.info(f"{'-'*20}Data Validation log completed.{'-'*20} \n\n")
        except Exception as e:
            raise AppException(e, sys) from e



    
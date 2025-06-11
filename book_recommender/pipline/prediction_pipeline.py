import pickle
import numpy as np
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException
import sys

class PredictionPipeline:
    def __init__(self, app_config=AppConfig()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
            self._load_resources()
        except Exception as e:
            raise AppException(e, sys) from e

    def _load_resources(self):
        self.book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
        self.final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))
        self.model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
        self.book_names = pickle.load(open(self.recommendation_config.book_name_serialized_objects, 'rb'))
        
        # Create title to details mapping
        self.book_details = {}
        for idx, row in self.final_rating.iterrows():
            title = row['title']
            self.book_details[title] = {
                'image_url': row['image_url'],
                'genre': row['genre'],
                'author': row['author'],
                'year': row['year'],
                'avg_rating': row['avg_rating']
                
            }

    def get_book_details(self, book_title):
        return self.book_details.get(book_title, {
            'image_url': "https://via.placeholder.com/150x200?text=No+Cover",
            'genre': "Unknown Genre",
            'author': "Unknown Author",
            'year': "N/A",
            'avg_rating': 0
        })

    def recommend_book(self, book_name):
        try:
            books_list = []
            book_id = np.where(self.book_pivot.index == book_name)[0][0]
            _, suggestion = self.model.kneighbors(
                self.book_pivot.iloc[book_id,:].values.reshape(1,-1), 
                n_neighbors=6
            )
            
            # Get details for all recommended books
            book_details_list = []
            for i in range(len(suggestion)):
                books = self.book_pivot.index[suggestion[i]]
                for j in books:
                    books_list.append(j)
                    book_details_list.append(self.get_book_details(j))
            
            return books_list, book_details_list
        
        except Exception as e:
            raise AppException(e, sys) from e
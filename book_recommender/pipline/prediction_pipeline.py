# book_recommender/pipline/prediction_pipeline.py
import os
import sys
import pickle
import numpy as np
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException

class PredictionPipeline:
    def __init__(self, app_config=AppConfig()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
            self._load_resources()
        except Exception as e:
            raise AppException(e, sys) from e

    def _load_resources(self):
        """Load all required resources once during initialization"""
        self.book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
        self.final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))
        self.model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
        self.book_names = pickle.load(open(self.recommendation_config.book_name_serialized_objects, 'rb'))

    def fetch_poster(self, suggestion):
        """Fetch poster URLs for book suggestions"""
        try:
            book_name = []
            ids_index = []
            poster_url = []

            for book_id in suggestion[0]:  # Handle 2D array
                book_name.append(self.book_pivot.index[book_id])

            for name in book_name:
                try:
                    ids = np.where(self.final_rating['title'] == name)[0][0]
                    ids_index.append(ids)
                except IndexError:
                    logging.warning(f"No match found for book: {name}")
                    continue

            for idx in ids_index:
                url = self.final_rating.iloc[idx]['image_url']
                # Handle missing covers
                poster_url.append(url if url.startswith('http') else 
                                "https://via.placeholder.com/150x200?text=No+Cover")
            
            return poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e

    def recommend_book(self, book_name):
        """Generate book recommendations"""
        try:
            books_list = []
            
            # Find book ID
            book_id = np.where(self.book_pivot.index == book_name)[0][0]
            
            # Get recommendations
            _, suggestion = self.model.kneighbors(
                self.book_pivot.iloc[book_id, :].values.reshape(1, -1), 
                n_neighbors=6
            )
            
            # Fetch posters
            poster_url = self.fetch_poster(suggestion)
            
            # Get book names
            for i in range(len(suggestion)):
                books = self.book_pivot.index[suggestion[i]]
                for j in books:
                    books_list.append(j)
                    
            return books_list, poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
import os
import sys
import pickle
import numpy as np
import streamlit as st
from book_recommender.logger.log import logging
from book_recommender.constants import *
from book_recommender.configuration.config import AppConfig
from book_recommender.exception.exception_handler import AppException
from book_recommender.pipline.training_pipeline import TrainingPipeline


class BookRecommender:
    def __init__(self, app_config=AppConfig()): # 'self': a personal ID card for each object created from the class
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e
        
    def fetch_poster(self, suggested_books):
        try:
            book_name = []
            idx_index = []
            book_poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_name_serialized_objects, 'rb'))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))

            for book in suggested_books:
                book_name.append(book_pivot.index[book])

            for name in book_name[0]:
                idx = np.where(final_rating['title'] == name)[0][0]
                idx_index.append(idx)
            
            for idx in idx_index:
                url = final_rating.iloc[idx]['image_url']
                book_poster_url.append(url)

            return book_poster_url

        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommend_books(self, book_name):
        try:

            books_list = []
            model = pickle.load(open(self.recommendation_config.trained_model_path,'rb'))
            book_pivot =  pickle.load(open(self.recommendation_config.book_pivot_serialized_objects,'rb'))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, indices = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

            book_poster_url = self.fetch_poster(indices)

            for i in range(len(indices)):
                books = book_pivot.index[indices[i]]
                for book in books:
                    books_list.append(book)

            return books_list, book_poster_url
        
        except Exception as e:
            raise AppException(e, sys) from e
        
    def train_model_engine(self):
        try:
            obj = TrainingPipeline()
            obj.start_training_pipeline()
            st.success("Model trained successfully!")
            logging.info("Recommended books successfully!")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def recommend_books_engine(self, selected_book_name):
        try:
            recommended_books, book_poster_url = self.recommend_books(selected_book_name)
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.text(recommended_books[1])
                st.image(book_poster_url[1])
            with col2:
                st.text(recommended_books[2])
                st.image(book_poster_url[2])
            with col3:
                st.text(recommended_books[3])
                st.image(book_poster_url[3])
            with col4:
                st.text(recommended_books[4])
                st.image(book_poster_url[4])
            with col5:
                st.text(recommended_books[5])
                st.image(book_poster_url[5])
            
        except Exception as e:
            raise AppException(e, sys) from e


if __name__ == "__main__":
    st.header("Book Recommender System - End-to-End")
    st.text("This is a book recommender system that uses collaborative filtering to recommend books based on user ratings.")

    obj = BookRecommender()

    # Train the model
    if st.button("Train the Model"):
        obj.train_model_engine()
    
    book_names = pickle.load(open(os.path.join(obj.recommendation_config.book_pivot_serialized_objects), 'rb'))
    selected_book_name = st.selectbox("Select a book to get recommendations", book_names)

    if st.button("Recommend Books"):
        obj.recommend_books_engine(selected_book_name)

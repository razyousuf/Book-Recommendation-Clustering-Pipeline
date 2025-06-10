# Your main Streamlit file (app.py)
import os
import sys
from pathlib import Path
import streamlit as st
import time
import random
from PIL import Image
from book_recommender.logger.log import logging
from book_recommender.configuration.config import AppConfig
from book_recommender.pipline.training_pipeline import TrainingPipeline
from book_recommender.pipline.prediction_pipeline import PredictionPipeline  # New import
from book_recommender.exception.exception_handler import AppException

# Configure page
st.set_page_config(
    page_title="End-to-End Book Recommender System",
    page_icon="📚",
    layout="centered"
    )
# Custom CSS for styling
st.markdown("""
    <style>
        .header { text-align: center; padding: 0.5rem; }
        .book-card { border-radius: 10px; padding: 1rem; transition: transform .2s; }
        .book-card:hover { transform: scale(1.03); background-color: #f9f9f9; }
        .section-title { border-bottom: 2px solid #4f8bf9; padding-bottom: 0.5rem; }
        .stButton>button { width: 80%; transition: all .2s; }
        .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# Header with logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("📚 End-to-End Book Recommender System")
    st.markdown("""
    <div style="color: #666; margin-top: -15px; margin-bottom: 10px;">
    Collaborative Filtering Recommendation Engine
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
trained_model_path = AppConfig().get_recommendation_config().trained_model_path
if 'trained' not in st.session_state:
    st.session_state.trained = Path(trained_model_path).exists()
if 'trained' not in st.session_state:
    st.session_state.trained = False
if 'show_recs' not in st.session_state:
    st.session_state.show_recs = False

# Training function
def train_model():
    try:
        with st.spinner('Training in progress... This may take several minutes'):
            start_time = time.time()
            trainer = TrainingPipeline()
            trainer.start_training_pipeline()
            st.session_state.trained = True
            training_time = time.time() - start_time
            st.success(f"Training completed in {training_time:.1f} seconds!")
    except Exception as e:
        st.error(f"Training failed: {str(e)}")

# Training section
with st.expander("⚙️ System Configuration", expanded=True):
    st.write("Train the recommendation engine to get started:")
    if st.button('Train Recommender System', key='train_btn'):
        train_model()

# Recommendation display function
def display_recommendations(recommended_books, poster_url, final_rating_df):
    """Display recommendations in a grid with cards and extract tags"""
    cols = st.columns(5, gap="large")
    top_tags = []

    for i in range(5):  # Show first 5 recommendations
        with cols[i]:
            st.markdown('<div class="book-card">', unsafe_allow_html=True)
            st.image(
                poster_url[i], 
                use_container_width=True,
                caption=recommended_books[i] if len(recommended_books[i]) < 30 else recommended_books[i][:27] + "...",
            )
            st.markdown(
                f"""<div style="text-align: center; margin-top: 10px;">
                {'⭐' * random.randint(3,5)}
                <span style="color: #888; font-size: 0.8em;">({random.randint(30,500)} reviews)</span>
                </div>""",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Extract tag from the final_rating_df if available
            book_title = recommended_books[i]
            if 'genre' in final_rating_df.columns:
                genre = final_rating_df[final_rating_df['title'] == book_title]['genre']
                if not genre.empty:
                    top_tags.extend(genre.values[0].split(',')[:3])  # Pick top 3 per book

    # Tag cloud based on actual genres
    if top_tags:
        st.markdown("---")
        st.subheader("More Like This")
        tag_html = " ".join([
            f"<span class='tag' style='font-size: {random.randint(14,24)}px; margin: 5px;'>{tag.strip()}</span>"
            for tag in set(top_tags)
        ])
        st.markdown(f"<div style='text-align: center;'>{tag_html}</div>", unsafe_allow_html=True)


# Main recommendation flow
if st.session_state.trained:
    st.markdown('<div class="section-title">📖 Book Selection</div>', unsafe_allow_html=True)
    
    # Initialize prediction pipeline
    predictor = PredictionPipeline()
    
    # Get book names
    book_names = list(predictor.book_names)
    
    selected_books = st.selectbox(
        "Search or select a book:",
        book_names,
        index=book_names.index("Tears of the Giraffe (No.1 Ladies Detective Agency)") 
        if "Tears of the Giraffe (No.1 Ladies Detective Agency)" in book_names else 0
    )

    rec_col, gap, info_col = st.columns([2, 1, 7])
    with rec_col:
        if st.button('🔍 GET Recommendations', type='primary'):
            st.session_state.show_recs = True
            st.session_state.selected_book = selected_books
    
    with info_col:
        if st.session_state.show_recs:
            st.info(f"Showing recommendations for: **{st.session_state.selected_book}**")

# Display recommendations
if st.session_state.show_recs and st.session_state.trained:
    st.markdown('<div class="section-title">🌟 Recommended For You</div>', unsafe_allow_html=True)
    
    try:
        predictor = PredictionPipeline()
        recommended_books, poster_url = predictor.recommend_book(st.session_state.selected_book)
        #display_recommendations(recommended_books[1:6], poster_url[1:6])  # Skip the first (selected book)
        display_recommendations(recommended_books[1:6], poster_url[1:6], predictor.final_rating)

    
    except Exception as e:
        st.error(f"🚨 Recommendation failed: {str(e)}")
        st.error("Please try another book or retrain the system")

# Footer
st.markdown("---")
st.caption("© 2025 Book Recommender Pro | Developed by Raz | Version 1.0.0")
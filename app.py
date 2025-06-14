import time
from pathlib import Path
import streamlit as st

# App config & pipelines
from book_recommender.configuration.config import AppConfig
from book_recommender.pipline.training_pipeline import TrainingPipeline
from book_recommender.pipline.prediction_pipeline import PredictionPipeline
from book_recommender.exception.exception_handler import AppException

# UI classes
from book_recommender.ui.components import (
                                            UIStyler,
                                            UIHeader,
                                            BookSelector,
                                            RecommendationHeader,
                                            UIFooter,
                                            BookCard
                                            )

# Initialize configuration
app_config = AppConfig()
recommendation_config = app_config.get_recommendation_config()

# Page configuration
st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="centered"
)


# Inject CSS
UIStyler.inject_css()

# --- Session State Initialization ---
if 'trained' not in st.session_state:
    model_exists = Path(recommendation_config.trained_model_path).exists()
    book_names_exist = Path(recommendation_config.book_name_serialized_objects).exists()
    st.session_state.trained = model_exists and book_names_exist

if 'show_recs' not in st.session_state:
    st.session_state.show_recs = False

if 'predictor' not in st.session_state:
    st.session_state.predictor = None

# --- Predictor Initialization ---
if st.session_state.trained and st.session_state.predictor is None:
    try:
        st.session_state.predictor = PredictionPipeline()
    except Exception as e:
        st.error(f"Failed to initialize predictor: {str(e)}")
        st.session_state.predictor = None

# Render header
UIHeader.render()

# Training logic
def train_model():
    try:
        with st.spinner('Training in progress... This may take several minutes'):
            start_time = time.time()
            trainer = TrainingPipeline()
            trainer.start_training_pipeline()
            st.session_state.trained = True
            st.session_state.predictor = PredictionPipeline()  # Load predictor immediately
            training_time = time.time() - start_time
            st.success(f"Training completed in {training_time:.1f} seconds!")
            st.balloons()
    except Exception as e:
        st.error(f"Training failed: {str(e)}")

# Training UI
with st.expander("⚙️ System Configuration", expanded=not st.session_state.trained):
    if st.session_state.trained:
        st.success("✅ Model is already trained and ready for recommendations!")
        st.caption("Retrain only if you have new data or want to update the model")
    else:
        st.warning("⚠️ Model is not trained yet. Click the button below to start training.")
        st.caption("Training may take several minutes depending on the dataset size")

    train_button_label = "🔁 Re-train Model" if st.session_state.trained else "🚀 Train Model"

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button(train_button_label, key='train_btn'):
            train_model()

    with col2:
        if Path(recommendation_config.trained_model_path).exists():
            st.download_button(
                label="📥 Export Model",
                data=open(recommendation_config.trained_model_path, "rb"),
                file_name="model.pkl"
            )


# Main flow
if st.session_state.trained:
    predictor = st.session_state.predictor
    if predictor is None:
        st.error("Predictor initialization failed. Please retrain the model.")
        st.stop()

    book_names = predictor.book_names
    selected_books = BookSelector.render(book_names)

    RecommendationHeader.render(
        st.session_state.selected_book if st.session_state.show_recs else "",
        len(book_names)
    )

# Recommendations
if st.session_state.show_recs and st.session_state.trained:
    st.markdown('<div class="section-title">🌟 Similar Books Recommended For You</div>', unsafe_allow_html=True)
    
    try:
        predictor = st.session_state.predictor
        recommended_books, book_details_list = predictor.recommend_book(st.session_state.selected_book)
        top_recommendations = recommended_books[1:6]
        top_details = book_details_list[1:6]
        cols = st.columns(5, gap="small")

        for i in range(5):
            with cols[i]:
                if i < len(top_recommendations):
                    #st.write("📦 DEBUG book_details:", top_details[i])
                    card_html = BookCard.render(
                        book_title=top_recommendations[i],
                        book_details=top_details[i],
                        index=i
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"🚨 Recommendation failed: {str(e)}")
        st.error("Please try another book or retrain the system")

# Footer
UIFooter.render()

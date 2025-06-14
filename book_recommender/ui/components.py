import streamlit as st
from html import escape

from .styles import MAIN_STYLES

class UIStyler:
    @staticmethod
    def inject_css():
        st.markdown(MAIN_STYLES, unsafe_allow_html=True)

class UIHeader:
    @staticmethod
    def render():
        st.markdown("""
        <div class="header h1-container">
            <h1>📚 Book Recommender MLOps</h1>
            <div class="subtitle">
                Discover personalised book recommendations powered by collaborative filtering—tailored to your literary tastes, from timeless classics to hidden gems.
                <span style="color: #888; font-size: 0.9rem;">Powered by machine learning to find your next great read.</span>
                <span style="background: #e0f7fa; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; color: #00796b;">
                    📊 ML-Powered·
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

class BookSelector:
    @staticmethod
    def render(book_names):
        st.markdown('<div class="section-title">📖 Book Selection</div>', unsafe_allow_html=True)

        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                selected_books = st.selectbox(
                    "Search or select a book:",
                    book_names,
                    index=0,
                    label_visibility="collapsed"
                )

            with col2:
                if st.button('🔍 Get Recommendations', type='primary', use_container_width=True):
                    st.session_state.show_recs = True
                    st.session_state.selected_book = selected_books

        return selected_books

class RecommendationHeader:
    @staticmethod
    def render(selected_book, book_count):
        if st.session_state.show_recs:
            st.markdown(
                f"""
                <div class="recommendation-header">
                    <div>
                        <span style="font-size: 0.9rem; opacity: 0.9;">Showing recommendations for:</span>
                        <div class="book-title">{selected_book}</div>
                    </div>
                    <div class="book-chip">
                        <span class="book-chip-icon">📚</span>
                        {book_count} books in catalog
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

class BookCard:
    @staticmethod
    def render(book_title, book_details, index):
        accent_colors = ["#4f8bf9", "#6a11cb", "#2575fc", "#2c3e50", "#1a237e"]
        border_color = accent_colors[index % len(accent_colors)]

        image_url = book_details.get('image_url', '')
        genre = book_details.get('genre', 'Unknown')
        author = book_details.get('author', 'Unknown')
        year = book_details.get('year', 'N/A')
        avg_rating = int(book_details.get('avg_rating', 0))
        num_rating = int(book_details.get('num_of_rating', 0))

        def avg_to_stars(avg_rating):
            if avg_rating < 2:
                return 1
            elif avg_rating < 4:
                return 2
            elif avg_rating < 6:
                return 3
            elif avg_rating < 8:
                return 4
            else:
                return 5

        star_count = max(0, min(5, avg_to_stars(avg_rating)))
        rating_stars = '⭐' * star_count

        display_title = (book_title[:25] + '..') if len(book_title) > 25 else book_title
        alt_title = escape(display_title)

        invalid_image = (not image_url or image_url.endswith(".gif"))

        if invalid_image:
            image_tag = f'<div class="book-cover-placeholder">{display_title}</div>'
        else:
            image_tag = f'<img src="{image_url}" alt="{alt_title}" style="height: 220px;">'

        return f"""
        <div class="book-card" style="border-top: 4px solid {border_color};">
            <div class="image-container">
                {image_tag}
            </div>
            <div class="title">
                {display_title}
            </div>
            <div class="genre">
                Genre: {genre}
            </div>
            <div class="rating">
                {rating_stars}({num_rating})
            </div>
            <div class="author-year">
                {author}({year})
            </div>
        </div>
        """

class UIFooter:
    @staticmethod
    def render():
        st.markdown("---")
        st.caption("© 2025 Book Recommender System | Designed and developed by Raz | Version 1.0.0")

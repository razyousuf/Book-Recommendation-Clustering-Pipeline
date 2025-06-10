import streamlit as st
from .styles import MAIN_STYLES

class UIStyler:
    @staticmethod
    def inject_css():
        st.markdown(MAIN_STYLES, unsafe_allow_html=True)

class UIHeader:
    @staticmethod
    def render():
        st.markdown("""
        <div class="header h1" style="text-align: center; margin-bottom: 2rem;">
            <h1>📚 Book Recommender System</h1>
            <div class="subtitle" style="color: #666;">Collaborative Filtering Recommendation Engine</div>
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
        border_color = accent_colors[index]

        image_url = book_details.get("image_url", "")
        image_tag = f'<img src="{image_url}" alt="{book_title}" style="height: 220px;">' if image_url else f'<div style="height: 220px; display: flex; align-items: center; justify-content: center;">{book_title}</div>'

        return f"""
        <div class="book-card" style="border-top: 4px solid {border_color};">
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                {image_tag}
            </div>
            <div style="font-weight: 500; font-size: 0.95rem; text-align: center;">
                Genre: {book_details['genre']}
            </div>
            <div class="book-details">
                {book_details['author']} ({book_details['year']})
            </div>
        </div>
        """

class UIFooter:
    @staticmethod
    def render():
        st.markdown("---")
        st.caption("© 2025 Book Recommender System | Designed and developed by Raz | Version 1.0.0")

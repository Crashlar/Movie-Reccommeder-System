import streamlit as st
import pickle
import os
import requests
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
api_key = os.getenv("POSTER_PATH_API")

# --- UTILITY FUNCTIONS ---

def fetch_poster(movie_id):
    
    """Fetches the poster URL from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error"

@st.cache_data
def get_featured_movies(_df):
    """Selects 5 random movies and caches them so they don't change on click."""
    return _df.sample(5)

# --- MAIN PAGE LOGIC ---

def main():
    st.title("📽️ Movie Recommender Engine")
    
    st.markdown("""
    Imagine you walk into a huge library filled with thousands of movies. 
    Finding the right one for your mood could feel overwhelming. 
    This system acts as your personal guide to the perfect film.
    """)

    # 1. Load Data
    movie_list_path = os.path.join('artifacts', 'movie_list.pkl')
    
    if not os.path.exists(movie_list_path):
        st.error("Model artifacts not found! Please run your training pipeline (app.py) first.")
        return

    movies = pickle.load(open(movie_list_path, 'rb'))

    # 2. Search Section
    st.subheader("🔎 Find a Movie")
    selected_movie_name = st.selectbox(
        "Search or select a movie:",
        movies['title'].values,
        index=None,
        placeholder="Search through 45,000+ movies..."
    )

    if st.button("Get Recommendations"):
        if selected_movie_name:
            st.session_state.selected_movie = selected_movie_name
            st.switch_page("pages/Movie_Details.py")
        else:
            st.warning("Please select a movie from the dropdown first!")

    st.divider()

    # 3. Featured Section (Random 5)
    st.subheader("🔥 Popular For You")
    
    # Get cached random movies
    featured_df = get_featured_movies(movies)
    cols = st.columns(5)

    for i in range(len(featured_df)):
        with cols[i]:
            movie_item = featured_df.iloc[i]
            
            # Show Poster
            poster_url = fetch_poster(movie_item['id'])
            st.image(poster_url, use_container_width=True)
            
            # Show Title (Truncated if too long)
            title = movie_item['title']
            display_title = (title[:18] + '..') if len(title) > 20 else title
            st.markdown(f"**{display_title}**")
            
            # View Details Button
            # Unique key is essential: 'home_' + id
            if st.button("View Details", key=f"home_{movie_item['id']}"):
                st.session_state.selected_movie = movie_item['title']
                st.switch_page("pages/Movie_Details.py")

if __name__ == "__main__":
    main()
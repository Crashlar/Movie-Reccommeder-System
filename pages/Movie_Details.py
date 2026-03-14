import streamlit as st
import pickle
import os
# Crucial for converting your overview format
import ast  
import requests
from src.recommender_system.pipelines.prediction_pipeline import PredictionPipeline
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("POSTER_PATH_API")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def main():
    st.set_page_config(page_title="Overview Detail", layout="wide")

    if "selected_movie" not in st.session_state or st.session_state.selected_movie is None:
        st.warning("Please select a movie from the Home page first.")
        if st.button("🏠 Back to Home"):
            st.switch_page("pages/Home.py")
        return

    # Load artifacts to get current movie details
    movies = pickle.load(open(os.path.join('artifacts', 'movie_list.pkl'), 'rb'))
    movie_data = movies[movies['title'] == st.session_state.selected_movie].iloc[0]

    st.title(f"🎬 {movie_data['title']}")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(fetch_poster(movie_data['id']), use_container_width=True)

    with col2:
        st.subheader("Movie Specifications")
        
        # Metadata Formatting
        year = str(movie_data['release_date'])[:4]
        st.write(f"📅 **Release Year:** {year}")
        st.write(f"⏱️ **Runtime:** {movie_data['runtime']} Minutes")
        
        genres = movie_data['genres']
        genre_text = ", ".join(ast.literal_eval(genres)) if isinstance(genres, str) and genres.startswith('[') else str(genres)
        st.write(f"🎭 **Genres:** {genre_text}")
        
        st.divider()

        # OVERVIEW CLEANING LOGIC
        st.write("### 📝 Overview")
        raw_overview = movie_data['overview']
        
        try:
            # Safely convert the string "['When', 'siblings'...]" into a list
            overview_list = ast.literal_eval(raw_overview)
            # Join the list into a clean paragraph
            overview_text = " ".join(overview_list)
        except:
            # Fallback if the format is already a string
            overview_text = raw_overview

        st.write(overview_text)

    st.divider()

    # Recommendations Section
    st.subheader("🌟 You Might Also Like")
    pipeline = PredictionPipeline()
    recs = pipeline.recommend(st.session_state.selected_movie)

    rec_cols = st.columns(5)
    for i in range(len(recs)):
        with rec_cols[i]:
            st.image(fetch_poster(recs[i]['id']))
            st.write(f"**{recs[i]['title']}**")
            if st.button("View", key=f"rec_{recs[i]['id']}"):
                st.session_state.selected_movie = recs[i]['title']
                st.rerun()

if __name__ == "__main__":
    main()
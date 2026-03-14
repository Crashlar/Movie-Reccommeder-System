import streamlit as st
import pickle
import os
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

st.set_page_config(page_title="Movie Matcher", layout="wide")

def main():

    st.set_page_config(page_title="Movie Recommander Engine", page_icon="📽️")
    st.title("Movie Recommander Engine" )
    st.text("""Imagine you walk into a huge library filled with thousands of movies. Finding the right one for your mood could feel overwhelming. That’s where the Movie Recommender System comes in—it acts like a friendly guide who knows your tastes and helps you pick the perfect film.

        1. Personalized Suggestions,
        2.Smart Discovery,
        3. Easy to Use,
        4. Saves Your Time
            """
            )
    
    # Load list
    movies = pickle.load(open(os.path.join('artifacts', 'movie_list.pkl'), 'rb'))
    selected_movie = st.selectbox("Select a movie:", movies['title'].values)

    if st.button('Recommend'):
        pipeline = PredictionPipeline()
        recs = pipeline.recommend(selected_movie)

        cols = st.columns(5)
        
        for i in range(5):
            with cols[i]:
                # 1. Fetch Poster
                st.image(fetch_poster(recs[i]['id']))
                
                # 2. Movie Title (Bold)
                st.markdown(f"### {recs[i]['title']}")
                
                # 3. Release Year & Runtime
                release_year = str(recs[i]['year'])[:4] 
                st.caption(f"📅 {release_year}  |  ⏱️ {recs[i]['runtime']} min")
                
                # 4. Genres (Formatted list)
                # Cleaning the list if it's still a list object
                # genre_list = recs[i]['genres']
                # if isinstance(genre_list, list):
                #     genre_text = ", ".join(genre_list)
                # else:
                #     genre_text = str(genre_list)
                
                # st.markdown(f"**Type:** {genre_text}")

if __name__ == "__main__":
    main()
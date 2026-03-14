import os
import sys
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.recommender_system.exception import RecommenderException
from src.recommender_system.logger import logging

class PredictionPipeline:
    def __init__(self):
        self.movie_list_path = os.path.join('artifacts', 'movie_list.pkl')
        self.vectors_path = os.path.join('artifacts', 'movie_vectors.pkl')

    def recommend(self, movie_title):
        try:
            # 1. Load artifacts
            movies = pickle.load(open(self.movie_list_path, 'rb'))
            vectors = pickle.load(open(self.vectors_path, 'rb'))

            # 2. Find the index of the requested movie
            # Handling case-sensitivity and stripping whitespace
            movie_index = movies[movies['title'].str.lower() == movie_title.lower()].index[0]
            
            # 3. Calculate similarity for ONLY this movie against all others
            # This is a 1 x 46000 operation (very fast)
            distances = cosine_similarity(vectors[movie_index], vectors)
            
            # 4. Sort and get top 5
            # distances[0] is the array of scores for the target movie
            movie_list = sorted(list(enumerate(distances[0])), reverse=True, key=lambda x: x[1])[1:6]
            
            
            recommendations = []
            
            for i in movie_list:
                temp_df = movies.iloc[i[0]]
                
                recommendations.append({
                    "title": temp_df['title'],
                    "id": temp_df['id'],
                    "year": temp_df['release_date'], 
                    "genres": temp_df['genres'],
                    "runtime": temp_df['runtime'],
                    "overview" : temp_df['overview']
                })
                
            return recommendations    
        except IndexError:
            return ["Movie not found in database."]
        except Exception as e:
            raise RecommenderException(e, sys)
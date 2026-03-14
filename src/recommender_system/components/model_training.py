import os
import sys
import pandas as pd
import pickle
from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity

from src.recommender_system.exception import RecommenderException
from src.recommender_system.logger import logging

@dataclass
class ModelTrainerConfig:
    # We save the vectors and the dataframe, NOT the full matrix
    movie_list_path = os.path.join('artifacts', 'movie_list.pkl')
    vectors_path = os.path.join('artifacts', 'movie_vectors.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, transformed_df_path, preprocessor_path):
        try:
            logging.info("Starting model training (Vector Export).")
            
            # 1. Load data
            df = pd.read_csv(transformed_df_path)
            
            # 2. Load the vectorizer
            with open(preprocessor_path, 'rb') as f:
                cv = pickle.load(f)

            # 3. Create vectors 
            # We keep it as a sparse matrix for memory efficiency
            vectors = cv.transform(df['tags'])
            
            logging.info("Saving movie list and vectors to artifacts.")
            os.makedirs(os.path.dirname(self.model_trainer_config.movie_list_path), exist_ok=True)

            # 4. Save the dataframe (to map indices to titles)
            with open(self.model_trainer_config.movie_list_path, 'wb') as f:
                pickle.dump(df, f)

            # 5. Save the vectors
            with open(self.model_trainer_config.vectors_path, 'wb') as f:
                pickle.dump(vectors, f)
            
            logging.info("Artifacts saved successfully.")
            return self.model_trainer_config.movie_list_path

        except Exception as e:
            raise RecommenderException(e, sys)
from src.recommender_system.exception import RecommenderException
from src.recommender_system.logger import logging

import pandas as pd
import numpy as np
import os
import sys
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    # Path where the processed data for the model will be stored
    transformed_data_path = os.path.join('data', "processed", 'transformed_df.csv')
    # Path where the vectorizer (preprocessor) object will be saved
    preprocessor_obj_file_path = os.path.join('data', "processed", 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def convert_ast(self, obj):
        """Converts string representation of list to actual list."""
        if isinstance(obj, str):
            return ast.literal_eval(obj)
        return obj
    
    def initiate_data_transformation(self, train_data_path):
        try:
            logging.info("Starting  data transformation for recommendation system.")
            
            # 1. Load your pre-cleaned experiment output
            df = pd.read_csv(train_data_path)
            columns_to_convert = ['genres', 'overview', "production_companies","production_countries" , 'keywords', 'cast', 'crew']

            for col in columns_to_convert:
                df[col] = df[col].apply(self.convert_ast)
            logging.info("Combining columns into 'tags' feature.")
            
            # 3. Create the 'tags' column 
            # We combine all text-based features into one DNA string for the movie
            df['tags'] = df['overview'] + df['genres'] + df['production_companies'] + df["production_countries"] + df['keywords'] + df['cast'] + df['crew']
            
            # 4. Clean up the dataframe
            # We only need the ID, Title, and Tags for the actual recommendation engine
            new_df = df[['id', 'title', 'tags', 'release_date', 'genres', 'runtime']]
            
            new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
            new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

            logging.info("Tags column and metadata preserved successfully.")

            # 5. Save the final processed DataFrame
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_data_path), exist_ok=True)
            new_df.to_csv(self.data_transformation_config.transformed_data_path, index=False)

            logging.info(f"Transformed dataframe saved to {self.data_transformation_config.transformed_data_path}")

            # 6. Initialize and Fit the Vectorizer
            # This converts words into a 5000-dimensional coordinate system
            logging.info("Vectorizing the tags.")
            cv = CountVectorizer(max_features=500, stop_words='english')
            # Note: We fit here to define our 'vocabulary', which the prediction pipeline will need
            cv.fit(new_df['tags'])

            # 7. Save the preprocessor (vectorizer) object
            with open(self.data_transformation_config.preprocessor_obj_file_path, 'wb') as f:
                pickle.dump(cv, f)
            
            logging.info("Preprocessor object (vectorizer) saved successfully.")

            return (
                self.data_transformation_config.transformed_data_path,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise RecommenderException(e, sys) 


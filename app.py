import sys
import os

from src.recommender_system.logger import logging
from src.recommender_system.exception import RecommenderException
from src.recommender_system.components.data_transformation import DataTransformation
from src.recommender_system.components.model_training import ModelTrainer
from src.recommender_system.pipelines.prediction_pipeline import PredictionPipeline

def run_pipeline():
    try:
        logging.info("--- Recommendation System Pipeline Started ---")

        # 1. Data Transformation
        # Path to your pre-cleaned CSV
        raw_data_path = os.path.join("data", "processed", "experiment1_output.csv")
        
        logging.info("Initiating Data Transformation...")
        data_transformation = DataTransformation()
        train_df_path, preprocessor_path = data_transformation.initiate_data_transformation(raw_data_path)
        logging.info(f"Transformation complete. Transformed data: {train_df_path}")

        # 2. Model Training (Vector Export)
        logging.info("Initiating Model Training (Vector Generation)...")
        model_trainer = ModelTrainer()
        # This saves movie_list.pkl and movie_vectors.pkl instead of a huge matrix
        movie_list_path = model_trainer.initiate_model_trainer(train_df_path, preprocessor_path)
        logging.info(f"Training complete. Artifacts saved in artifacts folder.")

        print("\n" + "="*30)
        print("PIPELINE SUCCESSFUL!")
        print("="*30 + "\n")

    except Exception as e:
        raise RecommenderException(e, sys)

def test_recommendation(movie_name):
    try:
        logging.info(f"Testing recommendation for: {movie_name}")
        pipeline = PredictionPipeline()
        recommendations = pipeline.recommend(movie_name)
        
        print(f"Top 5 Recommendations for '{movie_name}':")
        for i, movie in enumerate(recommendations, 1):
            print(f"{i}. {movie['title']} ({movie['year']})") 
            
    except Exception as e:
        raise RecommenderException(e, sys)
    


if __name__ == "__main__":
    try:
        # Step 1: Run the full training flow
        run_pipeline()

        # Step 2: Test it with a movie title from your dataset
        # (Make sure 'Toy Story' or your chosen movie exists in your CSV)
        test_recommendation("Toy Story")

    except Exception as e:
        logging.error(f"Application failed: {str(e)}")
        print(f"Error: {e}")
import sys
from src.recommender_system.logger import logging
from src.recommender_system.exception import RecommenderException
from src.recommender_system.components.data_ingestion import DataIngestion
from src.recommender_system.components.data_transformation import DataTransformation
from src.recommender_system.components.data_transformation import DataTransformationConfig


if __name__ == "__main__":
    try:
        logging.info("Application started")

        data_path = "data/processed/experiment1_output.csv" 
        
        # 2. Initialize the transformation component
        logging.info("Starting the Data Transformation via app.py")
        data_transformation = DataTransformation()
        
        # 3. Execute the transformation
        # This will create your 'tags', save the CSV, and export the preprocessor.pkl
        train_df_path, preprocessor_path = data_transformation.initiate_data_transformation(data_path)
        
        print(f"Transformation Complete!")
        print(f"Transformed Data saved at: {train_df_path}")
        print(f"Vectorizer saved at: {preprocessor_path}")
    
        logging.info("Application ended successfully")

    except Exception as e:
        logging.info("Custom Exception at app.py execution")
        raise RecommenderException(e, sys)
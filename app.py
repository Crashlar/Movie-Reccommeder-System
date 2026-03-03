import sys
from src.recommender_system.logger import logging
from src.recommender_system.exception import RecommenderException
from src.recommender_system.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    try:
        logging.info("Application started")

        # Run data ingestion
        data_ingestion = DataIngestion()
        saved_files = data_ingestion.initiate_data_ingestion()

        logging.info("Data Ingestion completed successfully")
        print("Saved files:", saved_files)

    except Exception as e:
        logging.error("Custom Exception occurred during ingestion")
        raise RecommenderException(e, sys)

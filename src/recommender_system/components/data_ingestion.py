import pandas as pd
import numpy as np
import os
import sys

from dataclasses import dataclass
from src.recommender_system.exception import RecommenderException
from src.recommender_system.logger import logging
from src.recommender_system.utils import load_data


@dataclass
class DataIngestionConfig:
    raw_data_dir: str = os.path.join("data", "raw")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion started")

        try:
            # Load all CSVs from Kaggle (dictionary {filename: dataframe})
            data_dict = load_data()
            logging.info("All CSVs loaded successfully from Kaggle")

            # Ensure raw directory exists
            os.makedirs(self.ingestion_config.raw_data_dir, exist_ok=True)

            # Save each CSV separately
            saved_files = []
            for filename, df in data_dict.items():
                save_path = os.path.join(self.ingestion_config.raw_data_dir, filename)
                df.to_csv(save_path, index=False, header=True)
                logging.info(f"Saved {filename} at {save_path}")
                saved_files.append(save_path)

            return saved_files

        except Exception as e:
            raise RecommenderException(e, sys)

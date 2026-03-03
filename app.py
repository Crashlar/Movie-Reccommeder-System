from src.recommender_system.logger import logging
from src.recommender_system.exception import RecommenderException
import sys

if __name__ == "__main__":
    logging.info("The execution has started")

    try:
        a = 1 / 0 
    except Exception as e:
        logging.info("Custom Exception")
        raise RecommenderException(e , sys)
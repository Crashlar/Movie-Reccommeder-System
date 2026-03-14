# Movie Recommender System

This project is a movie recommender system that suggests movies to users based on their preferences. It is built with Python and uses a content-based filtering approach. The front-end is created with Streamlit.

## Table of Contents

- [Movie Recommender System](#movie-recommender-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Architecture](#project-architecture)
  - [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
    - [Training Pipeline](#training-pipeline)
    - [Running the Application](#running-the-application)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Features

-   **Content-Based Filtering:** Recommends movies based on movie content (e.g., genre, director, cast).
-   **Web Interface:** An interactive web interface built with Streamlit to get recommendations.
-   **Scalable Pipeline:** Uses DVC for data versioning and has a structured pipeline for training and prediction.
-   **Containerized:** Can be deployed using Docker.

## Project Architecture

The project follows a modular architecture with a clear separation of concerns.

-   **Data Ingestion:** Fetches the raw data.
-   **Data Transformation:** Cleans and preprocesses the data.
-   **Model Training:** Trains the recommendation model.
-   **Prediction Pipeline:** Serves the model to provide recommendations.
-   **Web Application:** A Streamlit application for user interaction.

## Setup and Installation

To get the project up and running on your local machine, follow these steps.

### Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Conda](https://docs.conda.io/en/latest/miniconda.html)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Crashlar/Movie-Reccommeder-System.git
    cd Movie-Reccommeder-System
    ```

2.  **Create a Conda environment:**
    ```bash
    conda create -n recommender python=3.8 -y
    conda activate recommender
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up DVC:**
    Initialize DVC to pull the data.
    ```bash
    dvc pull
    ```

## Usage

### Training Pipeline

To run the model training pipeline:

```bash
python -m src.recommender_system.pipelines.training_pipeline
```

### Running the Application

To start the Streamlit web application:

```bash
streamlit run stream.py
```

This will start the web server, and you can access the application at `http://localhost:8501`.

## Project Structure

```
├───.dvc                # DVC files for data versioning
├───artifacts           # To store model and other artifacts
├───data                # Raw and processed data
├───logs                # Application logs
├───notebooks           # Jupyter notebooks for experiments
├───pages               # Streamlit pages
├───src
│   └───recommender_system
│       ├───components      # Core components for data ingestion, transformation, etc.
│       ├───pipelines       # Training and prediction pipelines
│       ├───exception.py    # Custom exceptions
│       ├───logger.py       # Logging configuration
│       └───utils.py        # Utility functions
├───app.py              # Main application file (likely for Flask/FastAPI if stream.py is separate)
├───stream.py           # Main file for the Streamlit app
├───requirements.txt    # Project dependencies
├───setup.py            # setup script for the project
├───Dockerfile          # For containerizing the application
└───Readme.md           # This file
```

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

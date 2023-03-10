# Airflow Customer Segmentation

## Dependencies

What things you need to install the software and how to install them:

- Python 3.7 or above
- Apache Airflow
- Any other dependencies required by the project, such as libraries, tools, etc.

## Installing

A step by step series of examples that tell you how to get the project up and running:

1. Install Python 3.7 or above.
2. Install Apache Airflow. You can do this by running the following command:

    ```bash
    pip install apache-airflow==2.3.3
    ```

3. Install any other dependencies required by the project. You can do this by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

4. Clone or download the project repository.

## Project Structure

```text
├── dags                                     // dags directory
├── logs                                     // logs directory
├── src
    ├── configs                              // configuration
        ├── __init__.py
        ├── config.py                        // general configuration
        ├── e_commerce_config.py             // e-commerce customer configuration
        └── mall_config.py                   // mall customer configuration
    ├── data                                 // data directory
        ├── __init__.py
        ├── e_commerce.csv                   // e-commerce customer data
        └── mall.csv                         // mall customer data
    ├── models                               // trained model directory
    ├── notebooks                            // jupyter notebook directory
    ├── utils
        ├── __init__.py                      
        ├── db.py                            // database functions
        └── helpers.py                       // helper functions
    ├── crawler.py                           // crawler
    ├── segmentation.py                      // get segmentation result and insert to elasticsearch
    └── training.py                          // training segmentation model
├── streamlit                                // streamlit application
    ├── __init__.py
    ├── app.py                               // streamlit application
    ├── Dockerfile                           // docker file
    └── requirements.txt                     // requirements file
├── .env                                     // environment variables
├── .flake8
├── .gitignore
├── .isort.cfg
├── autoscan.sh
├── docker-compose.yml                       // docker-compose file
├── Dockerfile                               // docker file
├── pyproject.toml                           
├── README.md                                // README.md file
└── requirements.txt                         // requirements file
```

## Running the auto format code before commit

```bash
chmod +x ./autoscan.sh
./autoscan.sh
```

## Running project with Docker

1. Install Docker and Docker Compose.
2. Create logs and plugins directory in airflow home directory.

    ```bash
    mkdir -p ./logs
    mkdir -p ./plugins
    ```

3. Create models and data folder in src directory.

    ```bash
    mkdir -p ./src/models
    mkdir -p ./src/data
    ```

4. Run the following command:

    ```bash
    docker-compose build
    docker-compose up -d
    ```

5. Open <http://localhost:8080/> in your browser to see airflow webserver.
6. Open <http://localhost:8501/> in your browser to see streamlit app.

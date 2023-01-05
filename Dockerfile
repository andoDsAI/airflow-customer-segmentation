FROM puckel/docker-airflow:latest

USER root

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy DAGs and other files
COPY ./dags/ /usr/local/airflow/dags/
COPY ./logs/ /usr/local/airflow/logs/
COPY ./src/ /usr/local/airflow/src/

ENV AIRFLOW_HOME=/usr/local/airflow

USER airflow

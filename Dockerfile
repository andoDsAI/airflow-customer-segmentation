FROM apache/airflow:2.3.3

USER root

# Install python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && pip3 install -r requirements.txt

# Copy DAGs and other files
COPY ./dags /opt/airflow/dags
COPY ./logs /opt/airflow/logs
COPY ./plugins /opt/airflow/plugins
COPY ./src /opt/airflow/src

ENV AIRFLOW_HOME=/opt/airflow

# Create airflow user and set permissions
RUN adduser airflow sudo

RUN chown -R airflow ${AIRFLOW_HOME}

USER airflow

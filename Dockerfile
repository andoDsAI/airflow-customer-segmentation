FROM apache/airflow:2.3.3

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy DAGs and other files
COPY ./dags /opt/airflow/dags
COPY ./logs /opt/airflow/logs
COPY ./plugins /opt/airflow/plugins
COPY ./src /opt/airflow/src
COPY .env /opt/airflow/.env

ENV AIRFLOW_HOME=/opt/airflow

# Create airflow user and set permissions
RUN adduser airflow sudo

RUN chown -R airflow ${AIRFLOW_HOME}

USER airflow

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

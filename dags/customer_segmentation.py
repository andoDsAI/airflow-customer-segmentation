import datetime
import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")
DAG_OWNER_NAME = "andoDsAI"
START_DATE = days_ago(1)
SCHEDULE_INTERVAL = "0 0 * * *"
ALERT_EMAIL = ["andoDsAI@gmail.com"]
NUM_RETRIES = 1
RETRY_DELAY = datetime.timedelta(minutes=5)

default_args = {
    "owner": DAG_OWNER_NAME,
    "depends_on_past": False,
    "start_date": START_DATE,
    "email": ALERT_EMAIL,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": NUM_RETRIES,
    "retry_delay": RETRY_DELAY,
}

dag = DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,
)

# crawl task
crawl_mall = BashOperator(
    task_id="crawl_mall_customer_data",
    bash_command=f"python3 {repo_path}/src/crawler.py --customer_type mall",
    dag=dag,
)

crawl_e_commerce = BashOperator(
    task_id="crawl_e_commerce_customer_data",
    bash_command=f"python3 {repo_path}/src/crawler.py --customer_type e_commerce",
    dag=dag,
)

# train task
train_mall_model = BashOperator(
    task_id="train_mall_customer_segmentation_model",
    bash_command=f"python3 {repo_path}/src/train.py --customer_type mall",
    dag=dag,
)

train_e_commerce_model = BashOperator(
    task_id="train_e_commerce_customer_segmentation_model",
    bash_command=f"python3 {repo_path}/src/train.py --customer_type e_commerce",
    dag=dag,
)

# get segmentation result task and insert to elastic search
mall_segmentation = BashOperator(
    task_id="mall_customer_segmentation",
    bash_command=f"python3 {repo_path}/src/segmentation.py --customer_type mall",
    dag=dag,
)

e_commerce_segmentation = BashOperator(
    task_id="e_commerce_customer_segmentation",
    bash_command=f"python3 {repo_path}/src/segmentation.py --customer_type e_commerce",
    dag=dag,
)

crawl_mall >> train_mall_model >> mall_segmentation
crawl_e_commerce >> train_e_commerce_model >> e_commerce_segmentation

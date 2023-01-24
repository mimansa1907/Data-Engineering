# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago


# TASK 1.1
#defining DAG arguments

# You can override them on a per-task basis during operator initialization
dag_args = {
    'owner': 'Mimansa',
    'start_date': days_ago(0),
    'email': ['mimansa@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# TASK 1.2
# define the DAG
dag = DAG(
    DAGid = 'ETL_toll_data',
    default_args = dag_args,
    description='Unzip folder and store in form of csv files',
    schedule_interval=timedelta(days=1),
)

# TASK 1.3
first_task = BashOperator(
    task_id='unzip_data',
    bash_command='sudo tar -zxvf /home/project/airflow/dags/finalassignment/tolldata.tgz -C  /home/project/airflow/dags/finalassignment/ | more fileformats.txt',
    dag=dag,
)

# TASK 1.4
second_task = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='echo \'RowId,Timestamp,Anonymized Vehicle number,Vehicle type\' > csv_data.csv | cut -d \',\' -f1-4 vehicle-data.csv  >> csv_data.csv',
    dag=dag,
)

#TASK 1.5
third_task = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='echo \'Number of axles,Tollplaza id,Tollplaza code\' > tsv_data.csv |  tr \'\t\' \',\' < tollplaza-data.tsv | cut -d \',\' -f5-7 >> tsv_data.csv',
    dag=dag,
)

# TASK 1.6
fourth_task = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='echo \'Type of Payment code,Vehicle Code\' > fixed_width_data.csv | grep -oP \'[A-Z]{3,}\sVC[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]\' payment-data.txt | tr \' \' \',\' >> fixed_width_data.csv ',
    dag=dag,
)

# TASK 1.7
fifth_task = BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag,
)

# TASK 1.8
sixth_task = BashOperator(
    task_id='transform_data',
    bash_command='sed \'s/[^,]*/\U&/2\' extracted_data.csv > transformed_data.csv',
    dag=dag,
)

first_task>>second_task>>third_task>>fourth_task>>fifth_task>>sixth_task
from datetime import timedelta, datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import SqlSensor
from config import path_to_remote_code

default_args = {
	'owner': 'iurii_nesterov',
	'start_date': datetime(year=2022, month=10, day=23, hour=3, minute=0, second=0),
	'email': ['nesterov.iurii.1993@gmail.com'],
	'retries': 1,
	'retry_delay': timedelta(minutes=15),
	'execution_timeout': timedelta(minutes=300),
}

dag = DAG(
	'DAG_name',
	catchup=False,
	default_args = default_args,
	schedule_interval = '0 11 * * 1-5',
	description = 'ETL'
)
today = '{{ execution_date.date() + macros.timedelta(days=1) }}'

sql_sensor_query = f"""
SELECT TOP 1
FROM my_table 
WHERE created_at = '{today}';
"""

sql_sensor = SqlSensor(
	task_id="sql_sensor",
	conn_id = my_conn,
	sql = sql_sensor_query,
	timeout = 3600,
	poke_interval=300,
	dag=dag
)

def run_python_script():
	import os
	import sys
	my_path = path_to_remote_code + '/repo.py'
	sys.path.append(my_path)
	os.chdir(my_path)
	from repo import main
	return main()

python_task = PythonOperator(
	task_id='python_task',
	python_callable = run_python_script,
	dag=dag
)

sql_sensor >> python_task
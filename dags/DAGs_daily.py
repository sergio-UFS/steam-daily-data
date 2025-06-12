from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from operators.get_data_players import get_data_players
from operators.cleaning_data_games import clean_data_games
from operators.insert_db import insert_db


with DAG("get_daily_data", start_date=datetime(2025, 6, 4), schedule_interval="@daily", catchup=False) as dag:
    task = PythonOperator(
        task_id="get_data_players",
        python_callable=get_data_players,
        dag=dag,
        provide_context=True
    )

    task_treatment = PythonOperator(
        task_id="treatment_data_players",
        python_callable=clean_data_games,
        dag=dag,
        provide_context=True
    )

    saving_db = PythonOperator(
        task_id="insert_db",
        python_callable=insert_db,
        dag=dag,
        provide_context=True
    )

    task >> task_treatment >> saving_db

import pandas as pd
from datetime import datetime
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # operators/
parent_dir = os.path.dirname(current_dir)  # dags/
code_dir = os.path.join(parent_dir, 'code')  # dags/code/
sys.path.append(code_dir)
from db_operations import save_data_daily

def insert_db():
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    df_games = pd.read_csv(f'./dags/data/steam_top_players_2025-06-10.csv')

    data_to_insert = df_games.to_records(index=False).tolist()

    save_data_daily(data_hoje, data_to_insert)

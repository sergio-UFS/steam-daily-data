import psycopg2
import dotenv
import pandas as pd
from datetime import datetime
import numpy as np

def load_env():
    """Load environment variables from a .env file."""
    dotenv.load_dotenv()

load_env()

conn = psycopg2.connect(
    host=dotenv.get_key(dotenv.find_dotenv(), "SERVER_IP"),
    port=dotenv.get_key(dotenv.find_dotenv(), "SERVER_PORT"),
    database="postgres",
    user="postgres", 
    password=dotenv.get_key(dotenv.find_dotenv(), "PASSWORD_DB")
)

def save_data_daily(date, data):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    df_games = pd.DataFrame(data, columns=[
        "id","rank","peak_players_day","current_players","name","developers","publishers","release_date","total_reviews",
        "positive_percentual","categories","genres","date"
    ])

    df_games = df_games.where(pd.notnull(df_games), None)
    df_games = df_games.applymap(lambda x: None if pd.isna(x) or x is np.nan else x)
    df_games['positive_percentual'] = df_games['positive_percentual'].fillna(0)
    df_games['total_reviews'] = df_games['total_reviews'].fillna(0)

    with conn.cursor() as cur:
        insert_query = """
            INSERT INTO steam_games (
                id,rank,peak_players_day,current_players,name,developers,publishers,release_date,
                total_reviews,positive_percentual,categories,genres,date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        for row in df_games.itertuples(index=False):
            cur.execute(insert_query, row)
        conn.commit()
    print(f"Data for {date} saved successfully to the database.")





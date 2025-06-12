import pandas as pd
import requests
from datetime import datetime
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))  # operators/
parent_dir = os.path.dirname(current_dir)  # dags/
code_dir = os.path.join(parent_dir, 'code')  # dags/code/
sys.path.append(code_dir)
import adjustingdetails as adj

def clean_data_games():
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    df_games = pd.read_csv(f'./dags/data/steam_top_players_{data_hoje}.csv')
    csv_games = pd.read_csv('./dags/data/steam_games.csv')

    df_null_treatment = df_games[df_games['name'].isnull()]

    for index, game_null in df_null_treatment.iterrows():
        url = f"https://store.steampowered.com/api/appdetails?appids={game_null['id']}&cc=us"
        response = requests.get(url)
        data = response.json()

        if data[str(game_null['id'])]['success']:
            new_game = adj.formatting_details(data[str(game_null['id'])]['data'])
            new_game['release_date'] = new_game['release_date'].strftime("%Y-%m-%d") if new_game['release_date'] else 'Not Released'
            csv_games = pd.concat([csv_games, pd.DataFrame([new_game])], ignore_index=True)
            new_game_rank = {'id': game_null['id'] ,'rank':game_null['rank'] ,'peak_players_day': game_null['peak_players_day'],'current_players':game_null['current_players'] ,'name':new_game['name'] ,'developers':new_game['developers'] ,
                        'publishers':new_game['publishers'],'release_date':new_game['release_date'],'total_reviews':new_game['total_reviews'],'positive_percentual':new_game['positive_percentual'],'categories':new_game['categories'],
                        'genres':new_game['genres'], 'date': data_hoje}
            df_games = pd.concat([df_games, pd.DataFrame([new_game_rank])], ignore_index=True)

    
    df_games = df_games.drop_duplicates(subset=['id'], keep='last')
    df_games = df_games.reset_index(drop=True)

    df_games.sort_values(by='rank', inplace=True)
    df_games.to_csv(f'./dags/data/steam_top_players_{data_hoje}.csv', index=False)
    csv_games.to_csv('./dags/data/steam_games.csv', index=False)
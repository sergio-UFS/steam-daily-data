import pandas as pd
import requests
from datetime import datetime


def get_data_players():

    df_games = pd.read_csv('./dags/data/steam_games.csv')

    url = "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1"

    response = requests.get(url)
    data = response.json()

    top_games = data["response"]["ranks"]

    raw_aggregation = pd.DataFrame(columns = ['id','rank','peak_players_day','current_players','name','developers','publishers','release_date','total_reviews','positive_percentual','categories','genres','date'])


    array_ids = df_games['steam_appid'].to_numpy()


    for game in top_games:
        if(game['appid'] in array_ids):
            game_info = df_games[df_games['steam_appid'] == game['appid']]
            new_game_rank = {'id': game['appid'] ,'rank':game['rank'] ,'peak_players_day': game['peak_in_game'] ,'current_players': game['concurrent_in_game'] ,'name':game_info['name'] ,'developers':game_info['developers'] ,
                        'publishers':game_info['publishers'],'release_date':game_info['release_date'],'total_reviews':game_info['total_reviews'],'positive_percentual':game_info['positive_percentual'],'categories':game_info['categories'],
                        'genres':game_info['genres'], 'date': datetime.now().strftime("%Y-%m-%d")}
            
            raw_aggregation = pd.concat([raw_aggregation, pd.DataFrame(new_game_rank)], ignore_index=True)
            
        else:
            new_game_rank = {'id': game['appid'] ,'rank':game['rank'] ,'peak_players_day': game['peak_in_game'] ,'current_players': game['concurrent_in_game'] ,'name':None ,'developers':None ,
                        'publishers':None,'release_date':None,'total_reviews':None,'positive_percentual':None,'categories':None,
                        'genres':None,'date': datetime.now().strftime("%Y-%m-%d")}
            raw_aggregation = pd.concat([raw_aggregation, pd.DataFrame([new_game_rank])])


    data_hoje = datetime.now().strftime("%Y-%m-%d")
    raw_aggregation.to_csv(f'./dags/data/steam_top_players_{data_hoje}.csv', index=False)

import requests
from datetime import datetime, timedelta
import pandas as pd
import json
from scripts.extra_functions.formatter import use_prime_position
from scripts.constants import API_KEY, games_url, stats_url



def date_yesterday(days=1):
    now = datetime.today()
    yester_date = now - timedelta(days=days)
    string_date = yester_date.strftime('%Y-%m-%d')
    return string_date

def call_games(date_yesterday): 
    today_date_url_param = f'?dates[]={date_yesterday}'
    headers = {
        "accept":"application/json",
        "Authorization":API_KEY
    }
    games = requests.get(url=games_url+today_date_url_param, headers=headers)
    
    print("=== GAMES RESULT ===")
    games_result = games.json()
    games_data = games_result["data"][0]
    # print(games_data)


    home_team_name = games_data["home_team"]["full_name"]
    home_team_score = games_data["home_team_score"]
    home_team_id = games_data["home_team"]["id"]
    print(f"HOME: {home_team_name}: {home_team_score} | (id:{home_team_id})")

    visitor_team_name = games_data["visitor_team"]["full_name"]
    visitor_team_score = games_data["visitor_team_score"]
    visitor_team_id = games_data["visitor_team"]["id"]
    print(f"AWAY: {visitor_team_name}: {visitor_team_score} | (id:{visitor_team_id})")

    
    # Put in another function next time
    # STATS
    today_game_id = games_data["id"]
    game_id_url_param = f'?game_ids[]={today_game_id}'

    stats = requests.get(url=stats_url + game_id_url_param , headers=headers)
    stats_result = stats.json()
    next_cursor = str(stats_result["meta"]["next_cursor"])
    stats2 = requests.get(url=stats_url + game_id_url_param + '&cursor=' + next_cursor, headers=headers)
    stats_result2 = stats2.json()


    print("==============================================================================")
    pd.set_option('display.max_colwidth', 100)

    df_stats_pg1 = pd.json_normalize(stats_result['data'],meta=['id'])
    df_stats_pg2 = pd.json_normalize(stats_result2['data'],meta=['id'])
    df_all_stats = pd.concat([df_stats_pg1, df_stats_pg2], ignore_index=True)

    df_take_cols = df_all_stats[['player.jersey_number', 'player.first_name', 'player.last_name', 'player.position', 'pts', 'team.id', 'team.full_name', 'game.id']]
    df_arranged = df_take_cols.sort_values(by=['team.full_name', 'player.position', 'pts'], ascending=False, ignore_index=True)
    df_arranged["player.position"] = df_arranged['player.position'].apply(use_prime_position)


    df_center_home = df_arranged.loc[(df_arranged['player.position'] == 'C') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(1)
    df_center_visitor = df_arranged.loc[(df_arranged['player.position'] == 'C') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(1)

    forward_count_home = forward_count_visitor = 2
    print("=== ===")
    print(df_center_home.empty)
    if df_center_home.empty:
        forward_count_home = 3
    elif df_center_visitor.empty:
        forward_count_visitor = 3

    df_forward_home = df_arranged.loc[(df_arranged['player.position'] == 'F') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(forward_count_home)
    df_forward_visitor = df_arranged.loc[(df_arranged['player.position'] == 'F') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(forward_count_visitor)

    df_guard_home = df_arranged.loc[(df_arranged['player.position'] == 'G') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(2)
    df_guard_visitor = df_arranged.loc[(df_arranged['player.position'] == 'G') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(2)    

    home_df = pd.concat([df_center_home, df_forward_home, df_guard_home], ignore_index=True)
    visitor_df = pd.concat([df_center_visitor, df_forward_visitor, df_guard_visitor], ignore_index=True)

    print(home_df, "\n", visitor_df)

    return [home_df, visitor_df]

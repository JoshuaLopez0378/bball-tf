import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from scripts.extra_functions.formatter import use_prime_position
from scripts.constants import API_KEY, games_url, stats_url

headers = {
    "accept":"application/json",
    "Authorization":API_KEY
}

def date_yesterday(days=1):
    now = datetime.today()
    yester_date = now - timedelta(days=days)
    string_date = yester_date.strftime('%Y-%m-%d')
    return string_date

def check_games(date_yesterday): 
    # Request prerequisites
    today_date_url_param = f'?dates[]={date_yesterday}'


    # Perform get request and take result
    request_games = requests.get(url=f"{games_url}{today_date_url_param}", headers=headers)
    print("=== ALL GAMES RESULT ===")
    request_games_result = request_games.json()
    request_games_data = request_games_result["data"]

    # List all games, "home vs away" format
    all_games_list = [f"{res[0] + 1} | {res[1]['home_team']['full_name']} VS {res[1]['visitor_team']['full_name']}" for res in enumerate(request_games_data)]
    # print(all_games_list)

    
    return all_games_list, request_games_data

def check_matchup(choice, request_games_data):
    while True:
        try:
            matchup_data = request_games_data[choice-1]

            home_team_name = matchup_data["home_team"]["full_name"]
            home_team_score = matchup_data["home_team_score"]
            home_team_id = matchup_data["home_team"]["id"]
            print(f"HOME: {home_team_name}: {home_team_score} | (id:{home_team_id})")

            visitor_team_name = matchup_data["visitor_team"]["full_name"]
            visitor_team_score = matchup_data["visitor_team_score"]
            visitor_team_id = matchup_data["visitor_team"]["id"]
            print(f"AWAY: {visitor_team_name}: {visitor_team_score} | (id:{visitor_team_id})")

            matchup_details = {
                "game_id": matchup_data['id'],
                "home": {
                    "team_name": home_team_name,
                    "team_score": home_team_score,
                    "team_id": home_team_id
                },
                "visitor": {
                    "team_name": visitor_team_name,
                    "team_score": visitor_team_score,
                    "team_id": visitor_team_id
                }
            }

            if home_team_score > visitor_team_score:
                matchup_details['team_win'] = home_team_id
            else:
                matchup_details['team_win'] = visitor_team_id
            
            json_matchup_details = json.dumps(matchup_details)
            return json_matchup_details

        except IndexError:
            print("Choice not exist")
            return "Choice not exist"

def check_team_stats(json_matchup_details):
    loaded_matchup_details = json.loads(json_matchup_details)

    # # STATS
    today_game_id = loaded_matchup_details['game_id']
    game_id_url_param = f'?game_ids[]={today_game_id}'

    stats = requests.get(url=f"{stats_url}{game_id_url_param}" , headers=headers)
    stats_result = stats.json()
    next_cursor = str(stats_result["meta"]["next_cursor"])
    stats2 = requests.get(url=stats_url + game_id_url_param + '&cursor=' + next_cursor, headers=headers)
    stats_result2 = stats2.json()

    df_stats_result = pd.json_normalize(stats_result['data'], meta=['id'])
    df_stats_result2 = pd.json_normalize(stats_result2['data'], meta=['id'])

    # print(df_stats_result)

    teams = pd.concat([df_stats_result, df_stats_result2], ignore_index=True)

    df_home_team = teams.loc[teams["team.id"] == loaded_matchup_details["home"]["team_id"]]
    df_home_team = df_home_team.copy()
    df_home_team.loc[:, ("home_visitor")] = "Home"

    df_visitor_team = teams.loc[teams["team.id"] == loaded_matchup_details["visitor"]["team_id"]]
    df_visitor_team = df_visitor_team.copy()
    df_visitor_team.loc[:, ("home_visitor")] = "Visitor"
    
    df_team_player_stats = pd.concat([df_home_team, df_visitor_team], ignore_index=True)
    filtered_df_team_player_stats = df_team_player_stats[["id", "min", "player.id", "player.first_name", "player.last_name", "pts", "player.position", "team.id", "team.full_name", "game.id", "game.date", "home_visitor"]]
    filtered_df_team_player_stats = filtered_df_team_player_stats.copy()
    filtered_df_team_player_stats.loc[:,("win")] = np.where(filtered_df_team_player_stats["team.id"] == loaded_matchup_details["team_win"], "Win" , "Lose")
    sorted_df_team_player_stats = filtered_df_team_player_stats.sort_values(by=["team.id", "player.position", "pts"], ascending=False, ignore_index=True)

    return sorted_df_team_player_stats


def check_top_5(stats_list, team_ids=0):
    pd.set_option('display.max_colwidth', 100)
    print("==============================================================================")
    stats_list["player.position"] = stats_list["player.position"].apply(use_prime_position)
    # print(stats_list)

    df_center_home = stats_list.loc[(stats_list["player.position"] == 'C') & (stats_list["team.id"] == team_ids["home"])].head(1)
    df_center_visitor = stats_list.loc[(stats_list["player.position"] == 'C') & (stats_list["team.id"] == team_ids["visitor"])].head(1)

    forward_count_home = forward_count_visitor = 2
    if df_center_home.empty:
        forward_count_home = 3
    elif df_center_visitor.empty:
        forward_count_visitor = 3

    df_forward_home = stats_list.loc[(stats_list["player.position"] == 'F') & (stats_list["team.id"] == team_ids["home"])].head(forward_count_home)
    df_forward_visitor = stats_list.loc[(stats_list["player.position"] == 'F') & (stats_list["team.id"] == team_ids["visitor"])].head(forward_count_visitor)

    df_guard_home = stats_list.loc[(stats_list["player.position"] == 'G') & (stats_list["team.id"] == team_ids["home"])].head(2)
    df_guard_visitor = stats_list.loc[(stats_list["player.position"] == 'G') & (stats_list["team.id"] == team_ids["visitor"])].head(2)

    home_df = pd.concat([df_center_home, df_forward_home, df_guard_home], ignore_index=True)
    visitor_df = pd.concat([df_center_visitor, df_forward_visitor, df_guard_visitor], ignore_index=True)

    # print(home_df, "\n", visitor_df)

    # df_stats_pg1 = pd.json_normalize(stats_result['data'],meta=['id'])
    # df_stats_pg2 = pd.json_normalize(stats_result2['data'],meta=['id'])
    # df_all_stats = pd.concat([df_stats_pg1, df_stats_pg2], ignore_index=True)

    # df_take_cols = df_all_stats[['player.jersey_number', 'player.first_name', 'player.last_name', 'player.position', 'pts', 'team.id', 'team.full_name', 'game.id']]
    # df_arranged = df_take_cols.sort_values(by=['team.full_name', 'player.position', 'pts'], ascending=False, ignore_index=True)
    # df_arranged["player.position"] = df_arranged['player.position'].apply(use_prime_position)


    # df_center_home = df_arranged.loc[(df_arranged['player.position'] == 'C') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(1)
    # df_center_visitor = df_arranged.loc[(df_arranged['player.position'] == 'C') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(1)

    # forward_count_home = forward_count_visitor = 2
    # print("=== ===")
    # print(df_center_home.empty)
    # if df_center_home.empty:
    #     forward_count_home = 3
    # elif df_center_visitor.empty:
    #     forward_count_visitor = 3

    # df_forward_home = df_arranged.loc[(df_arranged['player.position'] == 'F') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(forward_count_home)
    # df_forward_visitor = df_arranged.loc[(df_arranged['player.position'] == 'F') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(forward_count_visitor)

    # df_guard_home = df_arranged.loc[(df_arranged['player.position'] == 'G') & (df_arranged['team.id'] == home_team_id)].sort_values(by=['pts'], ascending=False).head(2)
    # df_guard_visitor = df_arranged.loc[(df_arranged['player.position'] == 'G') & (df_arranged['team.id'] == visitor_team_id)].sort_values(by=['pts'], ascending=False).head(2)    

    # home_df = pd.concat([df_center_home, df_forward_home, df_guard_home], ignore_index=True)
    # visitor_df = pd.concat([df_center_visitor, df_forward_visitor, df_guard_visitor], ignore_index=True)

    # print(home_df, "\n", visitor_df)

    home_visitor_df = pd.concat([home_df,visitor_df])

    return home_visitor_df

def check_winner_game(compared_list):
    check_win = compared_list.loc[compared_list["win"] == "Win"][["home_visitor","team.full_name"]].head(1)
    return check_win

def check_winner_position(compare_list):
    df_home = compare_list.loc[compare_list["home_visitor"] == "Home"]
    df_visitor = compare_list.loc[compare_list["home_visitor"] == "Visitor"]
    df_win = df_home.where(df_home["pts"] > df_visitor["pts"], df_visitor)
    
    return df_win

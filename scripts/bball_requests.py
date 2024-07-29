import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from scripts.extra_functions.formatter import use_prime_position
from scripts.constants import API_KEY, games_url, stats_url
from scripts.db_insert_values import insert_to_all_stats, insert_to_all_players, insert_to_all_games, insert_to_all_teams

headers = {
    "accept":"application/json",
    "Authorization":API_KEY
}

def date_yesterday(days=99): # Ideal 2024-04-24
    now = datetime.today()
    yester_date = now - timedelta(days=days)
    string_date = yester_date.strftime('%Y-%m-%d')
    return string_date

def check_games(date_yesterday): 
    # Request prerequisites
    today_date_url_param = f'?dates[]={date_yesterday}'


    # Perform get request and take result
    request_games = requests.get(url=f"{games_url}{today_date_url_param}", headers=headers)
    # print("=== ALL GAMES RESULT ===") ------------------------------
    request_games_result = request_games.json()
    request_games_data = request_games_result["data"]

    # For DB ------------------------------
    # print("------------------------------")
    # print(request_games_data)

    # List all games, "home vs away" format
    all_games_list = [f"{res[0] + 1} | {res[1]['home_team']['full_name']} VS {res[1]['visitor_team']['full_name']}" for res in enumerate(request_games_data)]
    # print(all_games_list)

    
    return all_games_list, request_games_data

def check_matchup(choice, request_games_data):
    while True:
        try:
            print("=== matchup data ===")
            print(request_games_data[choice-1])
            matchup_data = request_games_data[choice-1]
            home_team_name = matchup_data["home_team"]["full_name"]
            home_team_id = matchup_data["home_team"]["id"]

            visitor_team_name = matchup_data["visitor_team"]["full_name"]
            visitor_team_id = matchup_data["visitor_team"]["id"]

            
            matchup_details = {
                "game_id": matchup_data['id'],
                "home": {
                    "team_name": home_team_name,
                    "team_id": home_team_id
                },
                "visitor": {
                    "team_name": visitor_team_name,
                    "team_id": visitor_team_id
                }
            }

            teams = [matchup_details["home"]["team_name"], matchup_details["visitor"]["team_name"]]

            print("=== teams ===")
            print(teams)

            print("Choose team, enter ID")
            print([f"[{res[0] + 1}] {res[1]}" for res in enumerate(teams)])
            choice_team = int(input("Choice: "))
            user_team = teams[choice_team-1]
            teams.remove(user_team)
            opp_team = teams[0]
            del teams

            print(f"Choice: {user_team} ||| Opp: {opp_team}")
            # input("OK")
            # print("'========'")
            # print(matchup_data)


            home_team_score = matchup_data["home_team_score"]
            visitor_team_score = matchup_data["visitor_team_score"]

            matchup_details["home"]["home_team_score"] = home_team_score
            matchup_details["visitor"]["visitor_team_score"] = visitor_team_score

            # matchup_details = {
            #     "game_id": matchup_data['id'],
            #     "home": {
            #         "team_name": home_team_name,
            #         "team_score": home_team_score,
            #         "team_id": home_team_id
            #     },
            #     "visitor": {
            #         "team_name": visitor_team_name,
            #         "team_score": visitor_team_score,
            #         "team_id": visitor_team_id
            #     }
            # }

            if home_team_score > visitor_team_score:
                matchup_details['team_win'] = home_team_id
            else:
                matchup_details['team_win'] = visitor_team_id
            
            print("here")
            json_matchup_details = json.dumps(matchup_details)
            print(json_matchup_details)
            print("here2")
            # print("=======")
            # print(json_matchup_details)

            # print(user_games_details)
            # input("ok")

            return json_matchup_details

        except IndexError:
            print("Choice not exist")
            return "Choice not exist"

        except:
            print("Error")
            return "Error"

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
    teams_to_db = teams.copy()
    teams_to_db.columns = teams_to_db.columns.str.replace(".","_")
    # teams_to_db.set_index('id', inplace=True)

    # print("=======")
    # print(teams_to_db.columns)
    save_to_all_stats_list = ['id','min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'turnover', 'pf', 'pts', 'player_id', 'game_id']
    save_to_all_players_list = ['player_id', 'player_first_name', 'player_last_name','player_position', 'player_height', 'player_weight','player_jersey_number', 'player_college', 'player_country','player_draft_year', 'player_draft_round', 'player_draft_number','player_team_id']
    save_to_all_games_list = ['game_id', 'game_date', 'game_season', 'game_status', 'game_period','game_time', 'game_postseason', 'game_home_team_score','game_visitor_team_score', 'game_home_team_id', 'game_visitor_team_id']
    save_to_all_teams_list = ['team_id', 'team_conference', 'team_division','team_city', 'team_name', 'team_full_name', 'team_abbreviation']
    # teams.to_csv("teams_stats_return.csv", index=False)
    insert_to_all_players(teams_to_db[save_to_all_players_list])
    insert_to_all_teams(teams_to_db[save_to_all_teams_list])
    insert_to_all_games(teams_to_db[save_to_all_games_list])
    insert_to_all_stats(teams_to_db[save_to_all_stats_list])


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
    # print("==============================================================================") ------------------------------
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

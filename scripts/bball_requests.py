import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from scripts.constants import API_KEY, games_url
from scripts.db_insert_values import insert_to_user_stats, insert_to_all_games, insert_to_all_teams

headers = {
    "accept":"application/json",
    "Authorization":API_KEY
}

def date_yesterday(days=12): # Note: 2024-2025 season started Oct 22
    now = datetime.today()
    yester_date = now - timedelta(days=days)
    string_date = yester_date.strftime('%Y-%m-%d')
    return string_date

def check_games(date_yesterday):
    # Request prerequisites
    today_date_url_param = f'?dates[]={date_yesterday}'


    # Perform get request and take result
    request_games = requests.get(url=f"{games_url}{today_date_url_param}", headers=headers)
    request_games_result = request_games.json()
    request_games_data = request_games_result["data"]

    # print("-------------- DBATASBE ----------------")
    print(request_games_data)

    # List all games, "home vs away" format


    # insert_to_all_games(for_all_games_db_df)

    all_games_list = [f"{res[0] + 1} | {res[1]['home_team']['full_name']} VS {res[1]['visitor_team']['full_name']}" for res in enumerate(request_games_data)]
    # print(all_games_list)

    


    return all_games_list, request_games_data

def test_fxn(df, col):
    return df[col]

def check_matchup(choice, request_games_data):
    for_all_games_db_col = ["id", "date", "season", "status", "period", "time", "postseason", "home_team_score", "visitor_team_score"]

    all_games_df = pd.DataFrame(request_games_data)
    for_all_games_db_df = all_games_df[for_all_games_db_col]

    home_team_df = all_games_df["home_team"]
    visitor_team_df = all_games_df["visitor_team"]
    home_team_extract = home_team_df.apply(lambda id: id["id"])
    visitor_team_extract = visitor_team_df.apply(lambda id: id["id"])
    for_all_games_db_df["home_team_id"] = home_team_extract
    for_all_games_db_df["visitor_team_id"] = visitor_team_extract

    # print("-ok-")
    # print(home_team_df)
    all_teams_df_temp = pd.DataFrame([])

    save_to_all_teams_list = ['id', 'conference', 'division','city', 'name', 'full_name', 'abbreviation']
    for i in save_to_all_teams_list:
        all_teams_df_temp[i] = home_team_df.apply(test_fxn, col=i)
        all_teams_df_temp[i] = visitor_team_df.apply(test_fxn, col=i)

    insert_to_all_teams(all_teams_df_temp[save_to_all_teams_list])
    insert_to_all_games(for_all_games_db_df)

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

            teams = [{matchup_details["home"]["team_name"] : matchup_details["home"]["team_id"]}, {matchup_details["visitor"]["team_name"]:matchup_details["visitor"]["team_id"]}]

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
            
            print("here")
            json_matchup_details = json.dumps(matchup_details)
            print(json_matchup_details)
            print("here2")
            # print("=======")
            # print(json_matchup_details)

            # print(user_games_details)
            # input("ok")

            print("=== return choice ===")
            # user_game_id (increment)
            # team_id_choice
            user_team = list(user_team.values())[0]
            print(user_team)
            # team_id_opponent
            opp_team = list(opp_team.values())[0]
            print(opp_team)
            # is_choice_win
            is_choice_win = True if matchup_details['team_win'] == user_team else False
            print(is_choice_win)
            # is_choice_home
            is_choice_home = True if matchup_details['home']['team_id'] == user_team else False
            print(is_choice_home)
            # game_id
            print(matchup_details['game_id'])

            user_game_details = {
                "team_id_choice" : user_team,
                "team_id_opponent" : opp_team,
                "is_choice_win" : is_choice_win,
                "is_choice_home" : is_choice_home,
                "game_id" : matchup_details["game_id"]
            }

            # json_user_game_details = json.dumps(user_game_details)

            return json_matchup_details, user_game_details

        except IndexError:
            print("Choice not exist")
            return "Choice not exist"

        except:
            print("Error")
            return "Error"

def check_winner_game(json_matchup_details):
    check_win = json.loads(json_matchup_details)
    team_win = check_win["home"]["team_name"] if check_win["team_win"] == check_win["home"]["team_id"] else check_win["visitor"]["team_name"]
    print("====== team win =====")
    print(team_win)
    return team_win

def record_user_game(user_game_details):
    insert_to_user_stats(user_game_details)


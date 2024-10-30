import json
from scripts.bball_requests import date_yesterday, check_games, check_matchup, check_winner_game, record_user_game

print("Start")

string_date = date_yesterday()
all_games_list, request_games_data = check_games(string_date)
# """
print("Choose game, enter ID")
for game in all_games_list:
    print(game)
# """
choice = int(input("Choice: "))

json_matchup_details, user_game_details = check_matchup(choice, request_games_data)
json_matchup_details_load = json.loads(json_matchup_details)

team_ids = {"home": json_matchup_details_load["home"]["team_id"], "visitor": json_matchup_details_load["visitor"]["team_id"]}
# stats_list = check_team_stats(json_matchup_details)

print("===== JSON MATCHUP DETIALS ======")
print(json_matchup_details)
win_team = check_winner_game(json_matchup_details)
# node_request_game_win(win_team)

# node_request_player_win(win_position)

record_user_game(user_game_details)

print("End")
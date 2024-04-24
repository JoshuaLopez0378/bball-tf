import json
from scripts.bball_requests import date_yesterday, check_games, check_matchup, check_team_stats, check_top_5, check_winner_game, check_winner_position
from scripts.node_requests import node_request_game_win, node_request_player_win

print("Start")

string_date = date_yesterday()
all_games_list, request_games_data = check_games(string_date)
"""
print("Choose game, enter ID")
for game in all_games_list:
    print(game)
"""
choice = int(input("Choice: "))

json_matchup_details = check_matchup(choice, request_games_data)
json_matchup_details_load = json.loads(json_matchup_details)

team_ids = {"home": json_matchup_details_load["home"]["team_id"], "visitor": json_matchup_details_load["visitor"]["team_id"]}
stats_list = check_team_stats(json_matchup_details)
compared_list = check_top_5(stats_list, team_ids)

win_team = check_winner_game(compared_list)
node_request_game_win(win_team)

win_position = check_winner_position(compared_list)
node_request_player_win(win_position)

print("End")
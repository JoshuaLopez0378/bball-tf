import json
from scripts.bball_requests import date_yesterday, check_games, check_matchup
from scripts.node_requests import simulate_node_request, compare_team_stats

print("Start")

string_date = date_yesterday(2)
all_games_list, request_games_data = check_games(string_date)

print("Choose game, enter ID")
for game in all_games_list:
    print(game)
choice = int(input("Choice: "))

check_matchup(choice, request_games_data)
compared_list = compare_team_stats(stats_list)
simulate_node_request(compared_list)

print("End")
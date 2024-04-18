import json
from scripts.bball_requests import date_yesterday, check_games, check_matchup, check_team_stats
from scripts.node_requests import simulate_node_request, compare_team_stats

print("Start")

string_date = date_yesterday(2)
all_games_list, request_games_data = check_games(string_date)

print("Choose game, enter ID")
for game in all_games_list:
    print(game)
choice = int(input("Choice: "))

json_matchup_details = check_matchup(choice, request_games_data)
stats_list = check_team_stats(json_matchup_details)
# print(stats_list)
compared_list = compare_team_stats(stats_list)
print(compared_list)  
# simulate_node_request(compared_list)

print("End")
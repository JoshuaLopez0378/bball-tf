import json
from scripts.bball_requests import date_yesterday, check_games, check_matchup
from scripts.node_requests import compare_team_stats, simulate_node_request

print("Start")
### For test: 04/04/2024 <-- GSW has no C
string_date = date_yesterday(2)
all_games_list, request_games_data = check_games(string_date)

print("Choose game, enter ID")
for game in all_games_list:
    print(game)
choice = int(input("Choice: "))

check_matchup(choice, request_games_data)

# compared_list = compare_team_stats(stats_list)
# simulate_node_request(compared_list)

print("End")
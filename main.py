import json
from scripts.bball_requests import date_yesterday, call_games
from scripts.node_requests import compare_team_stats, simulate_node_request

print("Start")
### For test: 04/04/2024 <-- GSW has no C
string_date = date_yesterday(3)
stats_list = call_games(string_date)
compared_list = compare_team_stats(stats_list)
simulate_node_request(compared_list)

print("End")
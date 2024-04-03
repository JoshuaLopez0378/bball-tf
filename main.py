import json
from scripts.bball_requests import date_yesterday, call_games
from scripts.node_requests import compare_team_stats, simulate_node_request

print("Start")

string_date = date_yesterday()
stats_list = call_games(string_date)
compared_list = compare_team_stats(stats_list)
simulate_node_request(compared_list)

print("End")
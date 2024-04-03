import pandas as pd
import numpy as np

def compare_team_stats(stats_list):
    team_stats_list = stats_list
    df_home_team = team_stats_list[0]
    df_visitor_team = team_stats_list[1]
    
    df_diff = pd.DataFrame(df_home_team['player.position'])
    df_diff['Winner'] = pd.DataFrame(np.where(df_home_team['pts'] > df_visitor_team['pts'], 'Home', 'Visitor'))

    # print(df_diff)
    return df_diff
    
def simulate_node_request(compared_list):
    for index, row in compared_list.iterrows():
        if row["Winner"] == "Home":
            if row["player.position"] == "G":
                print("H-G")
            elif row["player.position"] == "F":
                print("H-F")
            else:
                print("H-C")
        elif row["Winner"] == "Visitor":
            if row["player.position"] == "G":
                print("V-G")
            elif row["player.position"] == "F":
                print("V-F")
            else:
                print("V-C")
    # print(compared_list)
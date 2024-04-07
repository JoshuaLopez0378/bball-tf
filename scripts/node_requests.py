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

# servo1 - servo6   C
# servo2 - servo7   F
# servo3 - servo8   F
# servo4 - servo9   G
# servo5 - servo10  G

def simulate_node_request(compared_list):
    for index, row in compared_list.iterrows():
        ind = index+1
        if row["Winner"] == "Home":
            if row["player.position"] == "G":
                print("H-G  |   ", end='')
            elif row["player.position"] == "F":
                print("H-F  |   ", end='')
            else:
                print("H-C  |   ", end='')
            print(f"servo{ind} up | servo{ind+5} down")                
        elif row["Winner"] == "Visitor":
            if row["player.position"] == "G":
                print("V-G  |   ", end='')
            elif row["player.position"] == "F":
                print("V-F  |   ", end='')
            else:
                print("V-C  |   ", end='')
            print(f"servo{ind} down | servo{ind+5} up")
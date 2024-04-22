import pandas as pd
import numpy as np
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
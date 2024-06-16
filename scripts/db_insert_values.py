import psycopg2 as pg
import pandas as pd 
from sqlalchemy import create_engine 

pg_conn = pg.connect(database = "bballtf", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)


def insert_to_all_stats(all_stats_list):
    sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'

    db_conn = create_engine(sql_connection)
    conn = db_conn.connect()
    all_stats_list.to_sql('all_stats', con=db_conn, if_exists='append', index=False)


def insert_to_all_players(all_players_list):
    orig_players_col = list(all_players_list.columns)
    renamed_players_col = dict(zip(orig_players_col[1:], ("_".join(col.split("_")[1:]) for col in orig_players_col[1:])))

    all_players_list = all_players_list.rename(columns = renamed_players_col, inplace = True).copy()
    print(all_players_list)
    sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'

    db_conn = create_engine(sql_connection)
    conn = db_conn.connect()
    all_players_list.to_sql('all_players', con=db_conn, if_exists='replace', index=False)

def insert_to_all_games(all_games_list):
    orig_games_col = list(all_games_list.columns)
    renamed_games_col = dict(zip(orig_games_col[1:], ("_".join(col.split("_")[1:]) for col in orig_games_col[1:])))

    all_games_list_copy = all_games_list.rename(columns = renamed_games_col, inplace = True)
    all_games_list_copy = all_games_list_copy.iloc[[0]].copy()
    sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'

    db_conn = create_engine(sql_connection)
    conn = db_conn.connect()
    all_games_list.to_sql('all_games', con=db_conn, if_exists='append', index=False)

def insert_to_all_teams():
    pass


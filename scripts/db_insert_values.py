import psycopg2 as pg
import pandas as pd 
from sqlalchemy import create_engine, exc

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

    all_players_list.rename(columns = renamed_players_col, inplace = True)

    # sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'

    # db_conn = create_engine(sql_connection)
    # conn = db_conn.connect()
    # all_players_list.to_sql('all_players', con=db_conn, if_exists='replace', index=False)

def insert_to_all_games(all_games_list):
    orig_games_col = list(all_games_list.columns)
    renamed_games_col = dict(zip(orig_games_col[1:], ("_".join(col.split("_")[1:]) for col in orig_games_col[1:])))
    all_games_list.rename(columns = renamed_games_col, inplace = True)
    
    games_record = all_games_list.head(1)
    data_type_list = ['string', 'string', 'int', 'string', 'int', 'string', 'bool', 'int', 'int', 'string', 'string']
    games_record = games_record.astype(dict(zip(games_record.columns,data_type_list)))

    print("dtypes")
    print(games_record.dtypes)
    print(games_record)


    sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'
    db_conn = create_engine(sql_connection)
    conn = db_conn.connect()

    try:
        games_record.to_sql('all_games', con=db_conn, if_exists='append', index=False)
    except exc.IntegrityError :
        print("HERE")
        print("INTEGRITY ERROR")
        # print(type(e).__name__)
        print(list(games_record))
        update_table('all_games', games_record.columns, games_record.values.tolist()[0])
    except Exception as e:
        print("GENERAL")
        print(type(e).__name__)

def insert_to_all_teams():
    pass


def update_table(table_name, list_of_cols, list_of_values):
    update_set = ",\n".join([f"{col} = '{val}'" for col,val in zip(list_of_cols[1:],list_of_values[1:])])

    sql_statement = f"""
        UPDATE {table_name}
        SET {update_set}
        WHERE {list_of_cols[0]} = {str(list_of_values[0])}::VARCHAR(16);
    """

    print(sql_statement)
    cur = pg_conn.cursor()
    cur.execute(sql_statement)

    pg_conn.commit()
    cur.close()
    pg_conn.close()

    print("=== DONE UPDATING ===")
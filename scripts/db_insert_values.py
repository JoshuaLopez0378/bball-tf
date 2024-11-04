import psycopg2 as pg
import pandas as pd 
from sqlalchemy import create_engine, exc
import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(f'{current_dir}/schemas/main_tables_all_schema.yaml', 'r') as file:
    all_schema = yaml.safe_load(file)


sql_connection = 'postgresql://postgres:postgres@localhost:5432/bballtf'
db_conn = create_engine(sql_connection)
# conn = db_conn.connect()



def insert_to_all_games(all_games_list):
    orig_games_col = list(all_games_list.columns)
    print("origgames")
    print(orig_games_col)
    renamed_games_col = dict(zip(orig_games_col[0:], ("_".join(col.split("_")[0:]) for col in orig_games_col[0:])))
    # renamed_games_col = dict(zip([col for col in all_schema['all_games']['dtypes_df']],
                                #  [all_schema['all_games']['dtypes_df'][col] for col in all_schema['all_games']['dtypes_df']]))
    print("=== RENAMIND ===")
    print(renamed_games_col)
    all_games_list.rename(columns = renamed_games_col, inplace = True)
    all_games_list.rename(columns = {"id" : "game_id"}, inplace=True)
    games_record = all_games_list.head(1)

    # === NOTE: 
    # Commented code snippet for astype, since workaround for data types was to put ''
    # when doing dictionary comprehension <- since sql also accepts values with ''
    # for any data type
    # UPDATE: astype applied only to teams and players tables for now
    # ===
    # data_type_list = ['string', 'string', 'int', 'string', 'int', 'string', 'bool', 'int', 'int', 'string', 'string']
    # games_record = games_record.astype(dict(zip(games_record.columns,data_type_list)))
    # print("dtypes")
    # print(games_record.dtypes)
    # print(games_record)
    
    print("== SQL ==")
    print(all_games_list)
    try:
        all_games_list.to_sql('all_games', con=db_conn, if_exists='append', index=False)
    except exc.IntegrityError :
        update_table('all_games', games_record.columns, games_record.values.tolist()[0])
    except Exception as e:
        print("GENERAL")
        print(type(e).__name__)


def insert_to_all_teams(all_teams_list):
    orig_teams_col = list(all_teams_list)
    renamed_teams_col = dict(zip(orig_teams_col[0:], ("_".join(col.split("_")[0:]) for col in orig_teams_col[0:])))
    all_teams_list.rename(columns = renamed_teams_col, inplace = True)
    all_teams_list.rename(columns = {"id" : "team_id"}, inplace=True)
    all_teams_list.drop_duplicates(inplace=True)

    # astypes = dict(zip([col for col in all_schema['all_teams']['dtypes_df']], 
    #                    [all_schema['all_teams']['dtypes_df'][col] for col in all_schema['all_teams']['dtypes_df']]))

    all_teams_list = all_teams_list.fillna(0)

    try:
        print("all teams try")
        print(all_teams_list)
        all_teams_list.to_sql('all_teams', con=db_conn, if_exists='append', index=False)
    except exc.IntegrityError :
        print("all teams exception")
        print(all_teams_list.values.tolist())
        for record in all_teams_list.values.tolist():
            update_table('all_teams', all_teams_list.columns, record)
    except Exception as e:
        print("GENERAL")
        print(type(e).__name__)

def insert_to_user_stats(user_game_details):
    print("==== insert to user stats ====")
    print(user_game_details)
    pd_user_game_details = pd.DataFrame(user_game_details, index=[0])
    print(pd_user_game_details)
    pd_user_game_details.to_sql('user_games', con=db_conn, if_exists='append', index=False)

def update_table(table_name, list_of_cols, list_of_values):
    pg_conn = pg.connect(database = "bballtf", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
    update_set = ",".join([f"{col} = '{val}'" for col,val in zip(list_of_cols[1:],list_of_values[1:])])

    sql_statement = f"""
        UPDATE {table_name}
        SET {update_set}
        WHERE {list_of_cols[0]} = {str(list_of_values[0])}::VARCHAR(16);
    """
    # print("=== sql statement ===")
    # print(sql_statement)
    cur = pg_conn.cursor()
    cur.execute(sql_statement)

    pg_conn.commit()
    cur.close()
    pg_conn.close()

    print(f"=== Done updating {table_name} | {list_of_values[0]} ===")



# def insert_to_all_stats(all_stats_list):
#     try:
#         all_stats_list.to_sql('all_stats', con=db_conn, if_exists='append', index=False)
#     except:
#         print("=== Stats already loaded ===")
#         return "stats already loaded"

# def insert_to_all_players(all_players_list):
#     orig_players_col = list(all_players_list.columns)
#     renamed_players_col = dict(zip(orig_players_col[1:], ("_".join(col.split("_")[1:]) for col in orig_players_col[1:])))
#     all_players_list.rename(columns = renamed_players_col, inplace = True)
#     all_players_list = all_players_list.replace("'","''", regex=True)

#     print(all_players_list)

#     astypes = dict(zip([col for col in all_schema['all_players']['dtypes_df']], 
#                        [all_schema['all_players']['dtypes_df'][col] for col in all_schema['all_players']['dtypes_df']]))

#     all_players_list = all_players_list.fillna(0).astype(astypes)

#     try:
#         all_players_list.to_sql('all_players', con=db_conn, if_exists='append', index=False)
#     except exc.IntegrityError :
#         for record in all_players_list.values.tolist():
#             update_table('all_players', all_players_list.columns, record)
#     except Exception as e:
#         print("GENERAL")
#         print(type(e).__name__)

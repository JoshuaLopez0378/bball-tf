# import yaml
# with open('scripts/schemas/main_tables_all_schema.yaml', 'r') as file:
#     test_read = yaml.safe_load(file)

# # print(test_read)
# # print(test_read["all_players"])
# for i in test_read['all_players']['dtypes_df']:
#     print(f" {i} | {test_read['all_players']['dtypes_df'][i]}")


# x = dict(zip([col for col in test_read['all_players']['dtypes_df']], [test_read['all_players']['dtypes_df'][col] for col in test_read['all_players']['dtypes_df']]))
# print(x)

# x = dict(zip([col for col in test_read['all_players']['dtypes_df']], [test_read['all_players']['dtypes_df'][col] for col in test_read['all_players']['dtypes_df']]))
# print(x)

from bb_flask.db import get_db
import psycopg2 as pg

try:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT *" " FROM user_accs")
    posts_res = cursor.fetchall()
    db.commit()
    print(posts_res)
except:
    pg_conn = pg.connect(
        database="bballtf",
        user="postgres",
        host="localhost",
        password="postgres",
        port=5432,
    )
    sql_statement = "select * from user_games"
    cur = pg_conn.cursor()
    cur.execute(sql_statement)
    res = cur.fetchall()
    print(res)

colsing = ["test", "1"]
coldoub = ["test", "2"]
print(colsing, coldoub)

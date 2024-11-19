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
    cursor.execute("SELECT *" " FROM user_accs username = 'z'")
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
    sql_statement = "select * from user_accs where username = 'z'"
    cur = pg_conn.cursor()
    cur.execute(sql_statement)
    res = cur.fetchall()
    print(res)

# colsing = ["test", "1"]
# coldoub = ["test", "2"]
# print(colsing, coldoub)
col = ["user_id", "username", "password"]
tup = (
    2,
    "c",
    "scrypt:32768:8:1$LJbQnisoRErDl8Ag$85e8e4f57540a9fbefc70f43d29077fce4c7b3c5ac36995a968ba8dfc7bc8a6e6f0f053ef1f5d34eccd777a79606f574b4c6d20e5fce16eab0643b49290e19ad",
)
tuplist = list(str(i) for i in tup)
# print(tuplist)
print(col)
print(tuplist)
# user_zip = [dict(zip(col, user)) for user in tuplist]
user_zip = {col[i]: tuplist[i] for i in range(len(col))}
print(user_zip)

import psycopg2 as pg
conn = pg.connect(database = "bballtf", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)


cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS all_players CASCADE;
    DROP TABLE IF EXISTS all_teams CASCADE;
    DROP TABLE IF EXISTS all_games CASCADE;
    DROP TABLE IF EXISTS all_stats CASCADE;        
""")
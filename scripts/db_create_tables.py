import psycopg2 as pg

conn = pg.connect(
    database="bballtf",
    user="postgres",
    host="localhost",
    password="postgres",
    port=5432,
)


cur = conn.cursor()

cur.execute(
    """
            CREATE TABLE IF NOT EXISTS all_teams(
                team_id VARCHAR(16) PRIMARY KEY,
                conference VARCHAR(16),
                division VARCHAR(16),
                city VARCHAR(16),
                name VARCHAR(24),
                full_name VARCHAR(32),
                abbreviation VARCHAR(8)
            );
            """
)

cur.execute(
    """
            CREATE TABLE IF NOT EXISTS all_games(
                game_id VARCHAR(16) PRIMARY KEY,
                date DATE,
                season INTEGER,
                status VARCHAR(8),
                period INTEGER,
                time VARCHAR(8),
                postseason BOOL,
                home_team_score INTEGER,
                visitor_team_score INTEGER,
                home_team_id VARCHAR(16) REFERENCES all_teams(team_id),
                visitor_team_id VARCHAR(16) REFERENCES all_teams(team_id)
            );
            """
)

cur.execute(
    """
            CREATE TABLE IF NOT EXISTS user_games(
                user_game_id SERIAL PRIMARY KEY,
                team_id_choice VARCHAR(16),
                team_id_opponent VARCHAR(16),
                is_choice_win BOOL,
                is_choice_home BOOL,
                game_id VARCHAR(16) REFERENCES all_games(game_id)
            );
            """
)

cur.execute(
    """
            CREATE TABLE IF NOT EXISTS user_accs(
                user_id VARCHAR(16) PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(256)
            );
            """
)

# Make the changes to the database persistent``
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()

import psycopg2 as pg
conn = pg.connect(database = "bballtf", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)


cur = conn.cursor()
# Execute a command

# cur.execute("""
#     DROP TABLE IF EXISTS all_players CASCADE;
#     DROP TABLE IF EXISTS all_teams CASCADE;
#     DROP TABLE IF EXISTS all_games CASCADE;
#     DROP TABLE IF EXISTS all_stats CASCADE;        
# """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_players(
                player_id VARCHAR(16) PRIMARY KEY,
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                position VARCHAR(8),
                height VARCHAR(8),
                weight INTEGER,
                jersey_number VARCHAR(4),
                college VARCHAR(32),
                country VARCHAR(32),
                draft_year INTEGER,
                draft_round INTEGER,
                draft_number INTEGER,
                team_id VARCHAR(4)
            );
            """)

cur.execute("""
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
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_teams(
                team_id VARCHAR(16) PRIMARY KEY,
                conference VARCHAR(16),
                division VARCHAR(16),
                city VARCHAR(16),
                name VARCHAR(24),
                full_name VARCHAR(32),
                abbreviation VARCHAR(8)
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_stats(
                id VARCHAR(16) PRIMARY KEY,
                min INTEGER,
                fgm INTEGER,
                fga INTEGER,
                fg_pct FLOAT,
                fg3m INTEGER,
                fg3a INTEGER,
                fg3_pct FLOAT,
                ftm INTEGER,
                fta INTEGER,
                ft_pct FLOAT,
                oreb INTEGER,
                dreb INTEGER,
                reb INTEGER,
                ast INTEGER,
                stl INTEGER,
                blk INTEGER,
                turnover INTEGER,
                pf INTEGER,
                pts INTEGER,
                player_id VARCHAR(16) REFERENCES all_players(player_id),
                game_id VARCHAR(16) REFERENCES all_games(game_id)
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS user_stats(
                user_id VARCHAR(16) PRIMARY KEY,
                num_of_guesses INTEGER,
                wins INTEGER,
                win_pct FLOAT
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS user_games(
                user_game_id VARCHAR(16) PRIMARY KEY,
                user_team_win_lose VARCHAR(8),
                team_id_choice VARCHAR(16),
                team_id_opponent VARCHAR(16),
                is_choice_home BOOL,
                game_id VARCHAR(16) REFERENCES all_games(game_id),
                user_id VARCHAR(16) REFERENCES user_stats(user_id)
            );
            """)


# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()


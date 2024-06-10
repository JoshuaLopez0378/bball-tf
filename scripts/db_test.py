import psycopg2 as pg
conn = pg.connect(database = "bbaltf", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)


cur = conn.cursor()
# Execute a command
cur.execute("""
            CREATE TABLE IF NOT EXISTS all_stats(
                id VARCHAR(12) PRIMARY KEY,
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
                player_id VARCHAR(12) UNIQUE,
                game_id VARCHAR(12) UNIQUE
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_players(
                player_id VARCHAR(12) PRIMARY KEY,
                first_name VARCHAR(16),
                last_name VARCHAR(16),
                position VARCHAR(4),
                height VARCHAR(4),
                weight INTEGER,
                jersey_number VARCHAR(3),
                college VARCHAR(16),
                country VARCHAR(16),
                draft_year INTEGER,
                draft_round INTEGER,
                draft_number INTEGER,
                team_id VARCHAR(3) UNIQUE,
                CONSTRAINT fk_player_id
                    FOREIGN KEY(player_id)
                        REFERENCES all_stats(player_id)
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_games(
                game_id VARCHAR(12) PRIMARY KEY,
                date DATE,
                season INTEGER,
                status VARCHAR(10),
                period INTEGER,
                time VARCHAR(6),
                postseason BOOL,
                home_team_score INTEGER,
                visitor_team_score INTEGER,
                home_team_id VARCHAR(3),
                visitor_team_id VARCHAR(3),
                CONSTRAINT fk_game_id
                    FOREIGN KEY(game_id)
                        REFERENCES all_stats(game_id)
            );
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS all_teams(
                team_id VARCHAR(3) PRIMARY KEY,
                conference VARCHAR(6),
                division VARCHAR(10),
                city VARCHAR(16),
                name VARCHAR(24),
                full_name VARCHAR(4),
                abbreviation VARCHAR(4),
                CONSTRAINT fk_team_id
                    FOREIGN KEY(team_id)
                        REFERENCES all_players(team_id)
            );
            """)
# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()


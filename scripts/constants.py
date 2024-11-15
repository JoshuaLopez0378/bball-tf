import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
games_url = "http://api.balldontlie.io/v1/games"
stats_url = "https://api.balldontlie.io/v1/stats"

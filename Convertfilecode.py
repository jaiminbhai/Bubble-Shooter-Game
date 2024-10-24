import json
import sqlite3
import zipfile

# Load the APK file
apk_file = 'RummyMoment.apk'
with zipfile.ZipFile(apk_file, 'r') as zip_ref:
    json_file = zip_ref.extract('assets/data.json')

# Load the JSON file
with open(json_file) as f:
    data = json.load(f)

# Connect to the SQLite database
conn = sqlite3.connect('rummy_moment.db')
cursor = conn.cursor()

# Create tables for the relevant data
tables = {
    'players': ['id INTEGER PRIMARY KEY', 'name TEXT', 'score INTEGER'],
    'games': ['id INTEGER PRIMARY KEY', 'game_id TEXT', 'player_id INTEGER', 'score INTEGER'],
    'cards': ['id INTEGER PRIMARY KEY', 'card_id TEXT', 'game_id INTEGER', 'player_id INTEGER']
}

for table_name, columns in tables.items():
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})')

# Extract and insert data into the tables
players = data['players']
for player in players:
    cursor.execute("INSERT INTO players (name, score) VALUES (?, ?)", (player['name'], player['score']))

games = data['games']
for game in games:
    cursor.execute("INSERT INTO games (game_id, player_id, score) VALUES (?, ?, ?)", (game['game_id'], game['player_id'], game['score']))

cards = data['cards']
for card in cards:
    cursor.execute("INSERT INTO cards (card_id, game_id, player_id) VALUES (?, ?, ?)", (card['card_id'], card['game_id'], card['player_id']))

# Commit the changes and close the connection
conn.commit()
conn.close()
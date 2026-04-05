import requests
import sqlite3
import json

'''
This script serves as the ETL pipeline for the Premier League dashboard.

It extracts data from TWO distinct sources:
1. External REST API (football-data.org) to fetch live match results.
2. Local JSON file ('teams_info.json') to fetch static team metadata (stadiums, founding years).

The script transforms the raw match data to calculate league standings (points, GD, form), 
merges it with the local metadata, and loads the enriched dataset into a local SQLite 
database ('premier_league.db').

Note on Security: The API key is hardcoded here for academic simplicity. In a production 
environment, using environment variables (.env) or a secure vault is highly recommended.

Usage: 
- Ensure the `requests` library is installed (`pip install requests`).
- Ensure 'teams_info.json' is located in the same directory.
- Execute the script using: `python script.py`
'''

API_KEY = "YOUR_API_KEY_HERE" # Replace with your actual API key from football-data.org
API_URL = "https://api.football-data.org/v4/competitions/PL/matches"

def fetch_matches():
    headers = {'X-Auth-Token' : API_KEY}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to clean team names by removing common suffixes like "FC" or "AFC"
def clean_name(name):
    suffixes = [" FC", " AFC", "AFC "]
    for s in suffixes:
        name = name.replace(s, "")
    return name.strip()

def transform_data(data):
    standings = {}
    matches = data.get('matches', [])
    matches = sorted(data.get('matches', []), key=lambda x: x['utcDate'])

    try:
        with open ('teams_info.json', 'r', encoding='utf-8') as f:
            extra_info = json.load(f)
    except Exception as e:
        print(f"Error loading teams_info.json: {e}")
        extra_info = {}

    for m in matches:
        if m['status'] != 'FINISHED':
            continue

        home_team = clean_name(m['homeTeam']['name'])
        away_team = clean_name(m['awayTeam']['name'])
        home_goals = m['score']['fullTime'].get('home', 0)
        away_goals = m['score']['fullTime'].get('away', 0)
        home_crest = m['homeTeam'].get('crest')
        away_crest = m['awayTeam'].get('crest')

        for team in [home_team, away_team]:
            if team not in standings:
                standings[team] = {
                    'played': 0, 'wins': 0, 'draws': 0,
                    'losses': 0, 'goalsFor': 0, 'goalsAgainst': 0,
                    'gd': 0, 'points': 0, 'form': [],
                    'crest': home_crest if team == home_team else away_crest
                }
        
        standings[home_team]['played'] += 1
        standings[away_team]['played'] += 1
        standings[home_team]['goalsFor'] += home_goals
        standings[home_team]['goalsAgainst'] += away_goals
        standings[away_team]['goalsFor'] += away_goals
        standings[away_team]['goalsAgainst'] += home_goals

        if home_goals > away_goals:
            standings[home_team]['wins'] += 1
            standings[home_team]['points'] += 3
            standings[away_team]['losses'] += 1
            standings[home_team]['form'].append('W')
            standings[away_team]['form'].append('L')
        elif home_goals < away_goals:
            standings[away_team]['wins'] += 1
            standings[away_team]['points'] += 3
            standings[home_team]['losses'] += 1
            standings[away_team]['form'].append('W')
            standings[home_team]['form'].append('L')
        else:
            standings[home_team]['draws'] += 1
            standings[away_team]['draws'] += 1
            standings[home_team]['points'] += 1
            standings[away_team]['points'] += 1
            standings[home_team]['form'].append('D')
            standings[away_team]['form'].append('D')
        
        standings[home_team]['gd'] = standings[home_team]['goalsFor'] - standings[home_team]['goalsAgainst']
        standings[away_team]['gd'] = standings[away_team]['goalsFor'] - standings[away_team]['goalsAgainst']
    
    sorted_table = []
    for team, stats in standings.items():
        stats['form_str'] = "".join(stats['form'][-5:])
        stats['name'] = team
        
        team_extra = extra_info.get(team, {"stadium": "N/A", "founded": "N/A"})
        stats['stadium'] = team_extra['stadium']
        stats['founded'] = team_extra['founded']

        sorted_table.append(stats)
    
    sorted_table.sort(key=lambda x: (x['points'], x['gd'], x['goalsFor']), reverse=True)
    return sorted_table

def load_to_db(table_data):
    conn = sqlite3.connect('premier_league.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS standings')

    cursor.execute('''
        CREATE TABLE standings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT,
            played INTEGER,
            wins INTEGER,
            draws INTEGER,
            losses INTEGER,
            goals_for INTEGER,
            goals_against INTEGER,
            gd INTEGER,
            points INTEGER,
            form TEXT,
            crest_url TEXT,
            stadium TEXT,
            founded TEXT
        )
    ''')

    for team in table_data:
        cursor.execute('''
            INSERT INTO standings (
                team_name, played, wins, draws, losses, 
                goals_for, goals_against, gd, points, form,
                crest_url, stadium, founded
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            team['name'], 
            team['played'], 
            team['wins'], 
            team['draws'], 
            team['losses'], 
            team['goalsFor'], 
            team['goalsAgainst'], 
            team['gd'], 
            team['points'],
            team['form_str'],
            team['crest'],
            team['stadium'],
            str(team['founded'])
        ))

    conn.commit()
    conn.close()
    print("\n[SUCCESS] Data saved to premier_league.db")

if __name__ == "__main__":
    print("Step 1: Fetching data...")
    raw_data = fetch_matches()
    
    if raw_data:
        print("Step 2: Transforming data...")
        processed_table = transform_data(raw_data)
        
        print("Step 3: Loading to Database...")
        load_to_db(processed_table)
    else:
        print("Error: Could not complete the pipeline.")
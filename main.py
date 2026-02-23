import requests
import json
import os

# הגדרות (החלף את המפתח במפתח שלך מ-RapidAPI)
RAPID_API_KEY = "YOUR_RAPIDAPI_KEY"
LEAGUE_ID = 140  # ID של La Liga ב-API-Football

def fetch_la_liga_highlights():
    """מושך תקצירים רק של הליגה הספרדית"""
    url = "https://www.scorebat.com/video-api/v3/"
    response = requests.get(url).json()
    # סינון רק למשחקים מספרד
    la_liga_matches = [m for m in response.get('response', []) if "SPAIN: La Liga" in m.get('competition', '')]
    return la_liga_matches

def fetch_teams_and_squads():
    """מושך מידע על כל הקבוצות והשחקנים בליגה"""
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    # משיכת רשימת הקבוצות
    teams_url = f"https://api-football-v1.p.rapidapi.com/v3/teams?league={LEAGUE_ID}&season=2025"
    teams_data = requests.get(teams_url, headers=headers).json().get('response', [])
    
    database = {}
    for item in teams_data:
        team = item['team']
        venue = item['venue']
        database[team['id']] = {
            "name": team['name'],
            "logo": team['logo'],
            "founded": team['founded'],
            "stadium": venue['name'],
            "city": venue['city'],
            "squad": [] # כאן ניתן להוסיף קריאה נוספת לשחקנים במידת הצורך
        }
    return database

def save_data():
    if not os.path.exists("data"): os.makedirs("data")
    
    all_data = {
        "highlights": fetch_la_liga_highlights(),
        "teams": fetch_teams_and_squads()
    }
    
    with open("data/laliga_db.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("La Liga Database Updated!")

if __name__ == "__main__":
    save_data()

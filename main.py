import os
import json
import requests
import hashlib
import xml.etree.ElementTree as ET

DATA_FOLDER = "data"

def get_fallback_logo(team_name):
    bg_colors = ["0D6EFD", "DC3545", "198754", "6610F2", "FD7E14", "000000"]
    team_hash = hashlib.md5(team_name.encode()).hexdigest()
    color_idx = int(team_hash, 16) % len(bg_colors)
    safe_name = requests.utils.quote(team_name)
    return f"https://ui-avatars.com/api/?name={safe_name}&background={bg_colors[color_idx]}&color=fff&size=200&bold=true"

def fetch_news():
    """מושך מבזקי חדשות מסקיי ספורטס"""
    news_items = []
    try:
        r = requests.get("https://www.skysports.com/rss/12040", timeout=10)
        root = ET.fromstring(r.content)
        for item in root.findall('./channel/item')[:10]: # 10 מבזקים אחרונים
            news_items.append(item.find('title').text)
    except Exception as e:
        print(f"News error: {e}")
        news_items = ["Live football updates available 24/7", "Check back for transfer news"]
    return news_items

def fetch_data():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # משיכת תקצירים
    try:
        response = requests.get("https://www.scorebat.com/video-api/v3/").json()
        raw_matches = response.get('response', [])
    except:
        raw_matches = []

    organized_data = {"highlights": {}, "news": fetch_news()}

    for item in raw_matches[:40]:
        comp = item.get("competition", "International")
        title = item.get("title", "")
        teams = title.split(' - ') if " - " in title else [title, "Opponent"]
        home_n, away_n = teams[0].strip(), teams[1].strip()

        match_entry = {
            "title": title,
            "date": item.get("date"),
            "embed_code": item.get("videos", [{}])[0].get("embed"),
            "url": item.get("matchviewUrl"),
            "home_team": {"name": home_n, "logo": get_fallback_logo(home_n)},
            "away_team": {"name": away_n, "logo": get_fallback_logo(away_n)}
        }
        if comp not in organized_data["highlights"]: organized_data["highlights"][comp] = []
        organized_data["highlights"][comp].append(match_entry)

    with open(f"{DATA_FOLDER}/highlights.json", "w", encoding="utf-8") as f:
        json.dump(organized_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_data()

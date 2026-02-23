import os
import json
import requests
from datetime import datetime
import urllib.parse
import re

# --- Configuration ---
SCOREBAT_API_URL = "https://www.scorebat.com/video-api/v3/"
# For live scores, we use API-Football. Requires an API key in GitHub Secrets.
LIVE_SCORES_API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY") 

OUTPUT_DIR = "docs"
BASE_URL = "https://YOUR_USERNAME.github.io/YOUR_REPO_NAME" # Update this later

def ensure_environment():
    """
    Fail-safe: Ensures the output directory exists.
    """
    try:
        if not os.path.exists(OUTPUT_DIR):
            print(f"Creating directory: {OUTPUT_DIR}")
            os.makedirs(OUTPUT_DIR)
    except Exception as e:
        print(f"Critical error during environment setup: {e}")
        exit(1)

def fetch_highlights():
    """
    Fetches the latest football highlights from ScoreBat API.
    """
    print("Fetching highlights from ScoreBat...")
    try:
        response = requests.get(SCOREBAT_API_URL, timeout=15)
        response.raise_for_status()
        return response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return []

def fetch_live_scores():
    """
    Fetches live scores if API key is provided, otherwise returns mock/empty data gracefully.
    """
    print("Fetching live scores...")
    if not API_FOOTBALL_KEY:
        print("Notice: API_FOOTBALL_KEY not found. Skipping live scores.")
        return []

    headers = {
        'x-apisports-key': API_FOOTBALL_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(LIVE_SCORES_API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live scores: {e}")
        return []

def sanitize_filename(name):
    """
    Converts a league name to a URL-friendly string.
    """
    clean_name = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower()
    return re.sub(r'[\s-]+', '-', clean_name)

def generate_html_head(title):
    """Generates the common HTML head and SEO tags."""
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - חדשות ספורט, תקצירים ותוצאות בזמן אמת.">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; font-family: Arial, sans-serif; }}
        .video-container {{ position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000; }}
        .video-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
        .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: none; }}
        .live-badge {{ color: red; font-weight: bold; animation: blink 2s infinite; }}
        @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
    </style>
</head>
<body>
"""

def generate_navbar(leagues):
    """Generates the navigation bar with dynamic league links."""
    nav_links = "".join([f'<li><a class="dropdown-item" href="{sanitize_filename(l)}.html">{l}</a></li>' for l in leagues[:15]])
    
    return f"""
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="index.html">⚽ ספורט היילייטס</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html">ראשי</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            סינון לפי ליגה
                        </a>
                        <ul class="dropdown-menu text-end" aria-labelledby="navbarDropdown">
                            {nav_links}
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
"""

def generate_highlights_grid(items):
    """Generates the HTML grid for video highlights."""
    if not items:
        return "<p class='text-center'>אין תקצירים זמינים כרגע.</p>"
        
    grid_html = '<div class="row">'
    for item in items:
        embed_code = item.get("videos", [{}])[0].get("embed", "")
        title = item.get("title", "Game Highlight")
        comp = item.get("competition", "General")
        date_str = item.get("date", "")
        
        grid_html += f"""
        <div class="col-md-6 col-lg-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">{title}</h5>
                    <p class="card-text text-muted small">{comp}</p>
                    <div class="video-container mb-3">{embed_code}</div>
                    <small class="text-secondary">עודכן: {date_str[:10]}</small>
                </div>
            </div>
        </div>
        """
    grid_html += '</div>'
    return grid_html

def generate_live_scores_section(live_data):
    """Generates the live scores HTML section."""
    if not live_data:
        return "<p class='text-muted'>אין משחקים חיים כרגע, או שמפתח ה-API חסר.</p>"
        
    html = '<div class="row mb-4">'
    for match in live_data:
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        goals_home = match['goals']['home']
        goals_away = match['goals']['away']
        elapsed = match['fixture']['status']['elapsed']
        
        html += f"""
        <div class="col-md-4">
            <div class="card border-danger mb-3">
                <div class="card-body text-center">
                    <span class="live-badge">LIVE {elapsed}'</span>
                    <h5 class="mt-2">{home} {goals_home} - {goals_away} {away}</h5>
                </div>
            </div>
        </div>
        """
    html += '</div>'
    return html

def build_static_pages(highlights, live_scores):
    """
    Compiles the data into static HTML files and a sitemap.
    """
    print("Building static HTML pages...")
    
    # Extract unique leagues
    leagues = list(set([item.get('competition') for item in highlights if item.get('competition')]))
    leagues.sort()

    # 1. Build Index Page
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(generate_html_head("ראשי - תקצירי ספורט"))
        f.write(generate_navbar(leagues))
        f.write('<div class="container">')
        f.write('<h2 class="mb-3">🔴 משחקים חיים</h2>')
        f.write(generate_live_scores_section(live_scores))
        f.write('<hr><h2 class="mb-3">📺 התקצירים האחרונים</h2>')
        f.write(generate_highlights_grid(highlights))
        f.write('</div><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script></body></html>')

    # 2. Build League Pages
    sitemap_urls = [f"{BASE_URL}/index.html"]
    
    for league in leagues:
        league_filename = f"{sanitize_filename(league)}.html"
        league_path = os.path.join(OUTPUT_DIR, league_filename)
        league_highlights = [item for item in highlights if item.get('competition') == league]
        
        with open(league_path, 'w', encoding='utf-8') as f:
            f.write(generate_html_head(f"תקצירים - {league}"))
            f.write(generate_navbar(leagues))
            f.write('<div class="container">')
            f.write(f'<h2 class="mb-4">תקצירים: {league}</h2>')
            f.write(generate_highlights_grid(league_highlights))
            f.write('</div><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script></body></html>')
        
        sitemap_urls.append(f"{BASE_URL}/{league_filename}")

    # 3. Build Sitemap.xml
    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in sitemap_urls:
            f.write(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{timestamp}</lastmod>\n  </url>\n')
        f.write('</urlset>')
    
    print(f"Build complete. Created index, {len(leagues)} league pages, and sitemap.")

def main():
    print("--- Static Site Generation Started ---")
    ensure_environment()
    
    highlights = fetch_highlights()
    live_scores = fetch_live_scores()
    
    build_static_pages(highlights, live_scores)
    print("--- Process Completed ---")

if __name__ == "__main__":
    main()

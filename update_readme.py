import json
import os
from datetime import datetime

# --- Configuration ---
HIGHLIGHTS_FILE = "data/sports_highlights.json"
LIVE_SCORES_FILE = "data/live_scores.json"
README_FILE = "README.md"

def generate_readme():
    print("Updating README.md with latest stats...")
    
    # Fail-safe: Check if data files exist
    if not os.path.exists(HIGHLIGHTS_FILE):
        print("Data file not found. Skipping README update.")
        return

    with open(HIGHLIGHTS_FILE, 'r', encoding='utf-8') as f:
        highlights = json.load(f)
    
    with open(LIVE_SCORES_FILE, 'r', encoding='utf-8') as f:
        live_scores = json.load(f)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Build the Content
    content = [
        "# 🏆 ספורט פלוס - פורטל תקצירים ותוצאות",
        f"\n> **עדכון אחרון:** {now} (מתעדכן אוטומטית כל 30 דקות)",
        "\n## 📊 סטטיסטיקות המערכת",
        f"- 📺 **תקצירים זמינים:** {len(highlights)}",
        f"- ⚽ **משחקים חיים כרגע:** {len(live_scores)}",
        "\n## 🎬 5 התקצירים האחרונים שהתווספו",
        "| משחק | ליגה | תאריך |",
        "| :--- | :--- | :--- |"
    ]

    # Add last 5 highlights to a table
    for item in highlights[:5]:
        content.append(f"| {item['title']} | {item['competition']} | {item['date'][:10]} |")

    content.append("\n---")
    content.append("\n### 🚀 איך זה עובד?")
    content.append("הפרויקט מבוסס על **GitHub Actions** ו-**Python**. המערכת סורקת APIs של ספורט, מעבדת את הנתונים ומגישה אותם דרך **GitHub Pages** ללא עלות שרת.")
    content.append("\n[🔗 לצפייה באתר החי והמלא](https://yourusername.github.io/your-repo-name/)")

    # Write to file
    try:
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        print("README.md updated successfully.")
    except Exception as e:
        print(f"Error writing README: {e}")

if __name__ == "__main__":
    generate_readme()

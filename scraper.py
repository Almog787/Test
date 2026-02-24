import json
import yt_dlp

def scrape_kindergarten_dashboard():
    all_results = {}
    ydl_opts = {
        'quiet': True, 
        'extract_flat': True, 
        'skip_download': True,
        'format': 'best'
    }

    # קטגוריות משופרות ומדויקות לפי סדר היום בגן
    categories = {
        "purim": "שירי פורים לילדים ופעוטות מחרוזת רשמי",
        "morning_circle": "שירי מפגש בוקר בוקר טוב לגן ילדים",
        "movement_play": "שירי הפעלה ותנועה מירב האוסמן אריאלה סביר",
        "israeli_classics": "שירי ילדות ישראלית קלאסיים מחרוזת",
        "relaxation_sleep": "מוזיקה שקטה למנוחה בגן ילדים",
        "story_time": "סיפורים לפני שינה לילדים מדובב"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for key, query in categories.items():
            print(f"🔄 אוסף תוכן לקטגוריית: {key}")
            items = []
            try:
                # איסוף 12 סרטונים איכותיים לכל קטגוריה
                info = ydl.extract_info(f"ytsearch12:{query}", download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            items.append({
                                "id": entry['id'],
                                "title": entry.get('title').split('|')[0].strip(), # ניקוי כותרות
                                "url": f"https://www.youtube.com/embed/{entry['id']}?rel=0"
                            })
                all_results[key] = items
            except Exception as e:
                print(f"Error in {key}: {e}")

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print("✅ הדשבורד המקצועי עודכן!")

if __name__ == "__main__":
    scrape_kindergarten_dashboard()

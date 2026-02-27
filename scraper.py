import json
import yt_dlp
import random

def generate_lesson_plan(category, title):
    """
    יוצר מערך שיעור בסיסי בהתאם לקטגוריה כדי שהאתר יציג את הכפתור.
    ניתן להרחיב את הלוגיקה הזו עם בינה מלאכותית בעתיד.
    """
    plans = {
        "purim": [
            "פעילות רעשנים: מחלקים רעשנים ומרעישים לפי קצב השיר. בבתים שקטים עוצרים ובפזמון מרעישים חזק.",
            "ריקוד פורים: עומדים במעגל, מתחפשים בדמיון וצועדים לפי המקצב. בכל פעם שמוזכרת דמות מהחג מבצעים תנועה אופיינית."
        ],
        "morning_circle": [
            "מפגש בוקר: יושבים במעגל. כל ילד מברך את החבר שלידו ב'בוקר טוב' עם תנועת יד תואמת לשיר.",
            "פעילות גוף: נוגעים באיברי הגוף המוזכרים בשיר ומבצעים מתיחות בוקר עדינות."
        ],
        "movement_play": [
            "הפעלה בתנועה: הילדים מתפזרים במרחב. כשהמוזיקה עוצרת מבצעים 'פסל' בפוזה מצחיקה.",
            "משחק קצב: מוחאים כפיים ומקישים על הברכיים לסירוגין לפי קצב המנגינה."
        ],
        "relaxation_sleep": [
            "זמן רגיעה: מכבים את האורות בחדר. הילדים שוכבים בעיניים עצומות ומתרגלים נשימות עמוקות עם המוזיקה.",
            "דמיון מודרך עדין: שוכבים בנוח ומדמיינים שאנחנו ענן שט בשמיים לפי צלילי הפסנתר."
        ],
        "story_time": [
            "דיון בעקבות הסיפור: לאחר הצפייה, נשאל את הילדים - מה היה הרגע שהכי אהבתם? ואיך הגיבור הרגיש?",
            "ציור סיפור: נבקש מהילדים לצייר את הדמות המועדפת עליהם מהסיפור שראינו."
        ],
        "israeli_classics": [
            "שיח מורשת: משוחחים על השירים שגם אבא ואמא הכירו כשהיו קטנים ומצטרפים לשירה בציבור."
        ]
    }
    
    # מחזיר מערך אקראי מהקטגוריה המתאימה, או None אם אין
    if category in plans:
        return random.choice(plans[category])
    return None

def scrape_kindergarten_dashboard():
    all_results = {}
    ydl_opts = {
        'quiet': True, 
        'extract_flat': True, 
        'skip_download': True,
        'format': 'best'
    }

    # קטגוריות משופרות
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
                # איסוף 12 סרטונים
                info = ydl.extract_info(f"ytsearch12:{query}", download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            # בניית האובייקט כולל מערך שיעור
                            items.append({
                                "id": entry['id'],
                                "title": entry.get('title').split('|')[0].strip(),
                                "url": f"https://www.youtube.com/embed/{entry['id']}?rel=0",
                                "lesson_plan": generate_lesson_plan(key, entry.get('title'))
                            })
                all_results[key] = items
            except Exception as e:
                print(f"Error in {key}: {e}")

    # שמירה בפורמט התואם לאתר החדש
    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    print("\n✅ הדשבורד עודכן בהצלחה!")
    print("📁 הקובץ 'streams.json' כולל כעת מערכי שיעור מובנים.")

if __name__ == "__main__":
    scrape_kindergarten_dashboard()

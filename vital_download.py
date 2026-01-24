import requests
from bs4 import BeautifulSoup
import os
import json
import time
import zipfile
from datetime import datetime

# Configuration
VITAL_LIST_URL = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/2"
BASE_DIR = "/home/yourusername/vital_articles/" # Change 'yourusername'
TEMP_DIR = os.path.join(BASE_DIR, "current_run") 
LOG_FILE = os.path.join(BASE_DIR, "download_log.json")
USER_AGENT = "VitalDownloader/1.0 (your_email@example.com)"

def get_article_list():
    response = requests.get(VITAL_LIST_URL, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    content = soup.find(id="mw-content-text")
    for link in content.find_all('a'):
        title = link.get('title')
        href = link.get('href')
        if title and href and href.startswith('/wiki/') and ':' not in title:
            if "Level/2" not in href:
                articles.append(title)
    return list(dict.fromkeys(articles))[:100]

def download_article(title):
    api_url = f"https://en.wikipedia.org/wiki/api/rest_v1/page/html/{title.replace(' ', '_')}"
    try:
        response = requests.get(api_url, headers={"User-Agent": USER_AGENT}, timeout=10)
        if response.status_code == 200:
            return response.text, response.headers.get('ETag')
    except Exception as e:
        print(f"Error downloading {title}: {e}")
    return None, None

def run_task():
    # Setup directories
    for d in [BASE_DIR, TEMP_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

    history = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            history = json.load(f)

    article_titles = get_article_list()
    new_history = {}
    any_changes = False

    for title in article_titles:
        content, etag = download_article(title)
        
        # Only save if the ETag (version) has changed
        if content and (title not in history or history[title] != etag):
            filename = f"{title.replace('/', '_').replace(' ', '_')}.html"
            with open(os.path.join(TEMP_DIR, filename), "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {title}")
            new_history[title] = etag
            any_changes = True
        else:
            new_history[title] = history.get(title)
        
        time.sleep(0.1)

    # --- Compression Logic ---
    if any_changes:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        zip_name = f"vital_articles_{timestamp}.zip"
        zip_path = os.path.join(BASE_DIR, zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(TEMP_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file)
                    os.remove(file_path) # Clean up individual HTML after zipping
        
        print(f"Successfully compressed updates into {zip_name}")
    else:
        print("No changes detected. No new zip created.")

    with open(LOG_FILE, 'w') as f:
        json.dump(new_history, f)

if __name__ == "__main__":
    run_task()

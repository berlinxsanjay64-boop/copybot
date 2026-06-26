import requests
import feedparser
import time
import json
import os

BOT_TOKEN = "8950782305:AAE3q6fS05uwZnMFmvUouTE8-DYsTUleYmA"
CHANNEL_ID = "@punterworld1"
SEEN_FILE = "seen_news.json"

RSS_FEEDS = [
    "https://www.cricbuzz.com/rss-feeds/cricket-news",
        "https://feeds.bbci.co.uk/sport/cricket/rss.xml",
            "https://timesofindia.indiatimes.com/rss/4719148.cms"
            ]

            def load_seen():
                if os.path.exists(SEEN_FILE):
                        with open(SEEN_FILE, "r") as f:
                                    return json.load(f)
                                        return []

                                        def save_seen(seen):
                                            with open(SEEN_FILE, "w") as f:
                                                    json.dump(seen, f)

                                                    def send_message(text):
                                                        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                                                            payload = {
                                                                    "chat_id": CHANNEL_ID,
                                                                            "text": text,
                                                                                    "parse_mode": "HTML"
                                                                                        }
                                                                                            requests.post(url, json=payload)

                                                                                            def fetch_and_post():
                                                                                                seen = load_seen()
                                                                                                    new_seen = seen.copy()
                                                                                                    
                                                                                                        for feed_url in RSS_FEEDS:
                                                                                                                try:
                                                                                                                            feed = feedparser.parse(feed_url)
                                                                                                                                        for entry in feed.entries[:5]:
                                                                                                                                                        link = entry.get("link", "")
                                                                                                                                                                        if link and link not in seen:
                                                                                                                                                                                            title = entry.get("title", "No Title")
                                                                                                                                                                                                                summary = entry.get("summary", "")
                                                                                                                                                                                                                                    message = f"🏏 <b>{title}</b>\n\n{summary}\n\n🔗 <a href='{link}'>Read More</a>"
                                                                                                                                                                                                                                                        send_message(message)
                                                                                                                                                                                                                                                                            new_seen.append(link)
                                                                                                                                                                                                                                                                                                time.sleep(2)
                                                                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                                                                    print(f"Feed error: {e}")
                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                        save_seen(new_seen)
                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                            print("NewsBot started...")
                                                                                                                                                                                                                                                                                                                                while True:
                                                                                                                                                                                                                                                                                                                                        fetch_and_post()
                                                                                                                                                                                                                                                                                                                                                print("Checked news, waiting 10 minutes...")
                                                                                                                                                                                                                                                                                                                                                        time.sleep(600)

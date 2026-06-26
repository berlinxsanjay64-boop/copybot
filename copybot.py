import requests
import json
import os
import time

BOT_TOKEN = "8921679384:AAG9Jqlyrl7vZq5oLvJgna5sizobjWxOjok"
SOURCE_CHANNEL = "@mglionline"
DEST_CHANNEL = "@punterfamilybyking"
LAST_ID_FILE = "last_message_id.json"

def load_last_id():
        if os.path.exists(LAST_ID_FILE):
                    with open(LAST_ID_FILE, "r") as f:
                                    return json.load(f).get("last_id", 0)
                            return 0

def save_last_id(last_id):
        with open(LAST_ID_FILE, "w") as f:
                    json.dump({"last_id": last_id}, f)

    def get_channel_messages():
            last_id = load_last_id()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": -1, "limit": 1}
    resp = requests.get(url, params=params)
    data = resp.json()

    return data

def forward_new_messages():
        last_id = load_last_id()

    # Use forwardMessage approach
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"offset": last_id + 1, "timeout": 10, "limit": 100}

    try:
                resp = requests.get(url, params=params, timeout=15)
                data = resp.json()
            except:
        return

                    if not data.get("result"):
                                return

    for update in data["result"]:
                update_id = update["update_id"]
                if "channel_post" in update:
                                post = update["channel_post"]
                                chat_username = post.get("chat", {}).get("username", "")
                                if chat_username.lower() == SOURCE_CHANNEL.replace("@", "").lower():
                                                    message_id = post.get("message_id")
                                                    text = post.get("text", "")
                                                    caption = post.get("caption", "")
                                                    photo = post.get("photo", None)
                                                    video = post.get("video", None)
                                                    document = post.get("document", None)

                if photo:
                                        file_id = photo[-1]["file_id"]
                                        requests.post(
                                            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                                            json={"chat_id": DEST_CHANNEL, "photo": file_id, "caption": caption}
                                        )
elif video:
                    file_id = video["file_id"]
                    requests.post(
                                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
                                                json={"chat_id": DEST_CHANNEL, "video": file_id, "caption": caption}
                    )
elif document:
                    file_id = document["file_id"]
                    requests.post(
                                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                                                json={"chat_id": DEST_CHANNEL, "document": file_id, "caption": caption}
                    )
elif text:
                    requests.post(
                                                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                                                json={"chat_id": DEST_CHANNEL, "text": text}
                    )

        last_id = update_id

    save_last_id(last_id)

if __name__ == "__main__":
        print("CopyBot started...")
    while True:
                try:
                                forward_new_messages()
                                time.sleep(3)
except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

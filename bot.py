# bot.py
import os
from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

# ----- CONFIG (reads from environment variables) -----
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # set this on Render
# ADMIN_IDS as comma separated list: "123,456,789"
ADMINS_ENV = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in ADMINS_ENV.split(",") if x.strip().isdigit()]
# ----------------------------------------------------

if not BOT_TOKEN:
    raise Exception("TELEGRAM_TOKEN not set in environment variables")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.ok, r.text
    except Exception as e:
        return False, str(e)

def format_new_user(user_obj, group_name):
    first = user_obj.get("first_name", "")
    last = user_obj.get("last_name", "")
    username = user_obj.get("username", "")
    uid = user_obj.get("id", "")
    name = (first + (" " + last if last else "")).strip() or "(sem nome)"
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    username_display = f"@{username}" if username else "(sem username)"
    text = (
        f"👤 *Novo membro no grupo*\n\n"
        f"👥 *Grupo:* {group_name}\n"
        f"📛 *Nome:* {name}\n"
        f"💬 *Username:* {username_display}\n"
        f"🆔 *ID:* `{uid}`\n"
        f"⏰ *Entrou em:* {now}"
    )
    return text

@app.route("/", methods=["GET"])
def index():
    return "Bot rodando!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    # Telegram sends updates in "message" or other fields
    message = data.get("message") or data.get("edited_message")
    if not message:
        return "ok", 200

    # new_chat_members event
    new_members = message.get("new_chat_members")
    if new_members:
        group_name = message.get("chat", {}).get("title", "(sem título)")
        for user in new_members:
            text = format_new_user(user, group_name)
            for admin in ADMIN_IDS:
                send_message(admin, text)

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

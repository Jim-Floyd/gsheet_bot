import os
import openai
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# API keys
OPENAI_KEY = os.environ.get("OPENAI_KEY")      # ChatGPT API
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")  # DeepSeek API

openai.api_key = OPENAI_KEY

# Oddiy yoki murakkab savolni ajratish
def is_complex_question(text):
    keywords = ["sumifs", "query", "regex", "arrayformula", "pivot", "multi", "bir nechta"]
    return any(word in text.lower() for word in keywords)

def ask_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(url, json=data, headers=headers)
    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "DeepSeek API xatosi."

def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# Telegram bot komandasi
def start(update, context):
    update.message.reply_text("Salom! Google Sheets formulalari bo‘yicha yordam beraman. Savol beravering 😊")

def answer(update, context):
    text = update.message.text
    if is_complex_question(text):
        reply = ask_chatgpt(f"Google Sheets formulasi yoz: {text}")
    else:
        reply = ask_deepseek(f"Google Sheets formulasi yoz: {text}")
    update.message.reply_text(reply)

def main():
    updater = Updater(os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, answer))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

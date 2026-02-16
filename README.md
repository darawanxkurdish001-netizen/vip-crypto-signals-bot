# vip-crypto-signals-bot
import requests
import schedule
import time
import random
from telegram import Bot

TOKEN = "8542082295:AAEZJMhyUojouhyIyUy6QyaZTh-4W5wbf3U"
CHAT_ID = "768442747"

bot = Bot(token=TOKEN)

symbols = [
    "BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT",
    "DOGEUSDT","ADAUSDT","AVAXUSDT","DOTUSDT",
    "SHIBUSDT","PEPEUSDT","TRXUSDT","TONUSDT"
]

def generate_signal():
    symbol = random.choice(symbols)
    side = random.choice(["BUY","SELL"])
    entry = round(random.uniform(0.1,100),4)
    tp = round(entry * random.uniform(1.01,1.05),4)
    sl = round(entry * random.uniform(0.95,0.99),4)

    text = f"""
🔥 VIP CRYPTO SIGNAL 🔥

Pair: {symbol}
Side: {side}

Entry: {entry}
Take Profit: {tp}
Stop Loss: {sl}

#VIP #CRYPTO
"""
    bot.send_message(chat_id=CHAT_ID, text=text)

schedule.every().day.at("19:00").do(generate_signal)
schedule.every().day.at("20:00").do(generate_signal)
schedule.every().day.at("21:00").do(generate_signal)
schedule.every().day.at("22:00").do(generate_signal)
schedule.every().day.at("23:00").do(generate_signal)

while True:
    schedule.run_pending()
    time.sleep(30)

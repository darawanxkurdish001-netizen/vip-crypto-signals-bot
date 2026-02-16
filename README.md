import telebot
import requests
import pandas as pd
import ta
import threading
import time
import random
from datetime import datetime

TOKEN = "8542082295:AAEZJMhyUojouhyIyUy6QyaZTh-4W5wbf3U"
ADMIN_ID = 768442747

bot = telebot.TeleBot(TOKEN)
vip_users = set()

BIG_COINS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT"]
SMALL_COINS = ["XRPUSDT","ADAUSDT","DOGEUSDT","TRXUSDT","MATICUSDT","SHIBUSDT"]

SIGNAL_HOURS = [19,20,21,22,23]

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()
    closes = [float(c[4]) for c in data]
    return pd.DataFrame(closes, columns=["close"])

def choose_symbol():
    coins = BIG_COINS + SMALL_COINS
    random.shuffle(coins)
    for c in coins:
        price = get_price(c)
        if c in SMALL_COINS and price > 10:
            continue
        return c
    return random.choice(BIG_COINS)

def generate_signal():
    symbol = choose_symbol()
    df = get_klines(symbol)
    rsi = ta.momentum.RSIIndicator(df["close"], window=14).rsi().iloc[-1]
    price = df["close"].iloc[-1]

    if rsi < 30:
        side = "BUY"
        tp = price * 1.03
        sl = price * 0.97
    elif rsi > 70:
        side = "SELL"
        tp = price * 0.97
        sl = price * 1.03
    else:
        return None

    return (
        f"📊 VIP CRYPTO SIGNAL\n\n"
        f"Pair: {symbol}\n"
        f"Type: {side}\n"
        f"Price: {price:.4f}\n"
        f"TP: {tp:.4f}\n"
        f"SL: {sl:.4f}\n"
        f"RSI: {rsi:.1f}\n"
        f"Time: {datetime.now().strftime('%H:%M')}"
    )

def scheduler():
    sent_today = set()
    while True:
        now = datetime.now()
        h = now.hour

        if h in SIGNAL_HOURS and h not in sent_today:
            signal = generate_signal()
            if signal:
                for uid in vip_users:
                    try:
                        bot.send_message(uid, signal)
                    except:
                        pass
            sent_today.add(h)

        if h == 0:
            sent_today.clear()

        time.sleep(60)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "📈 VIP Crypto Signals Bot")

@bot.message_handler(commands=['vip'])
def add_vip(msg):
    if msg.from_user.id == ADMIN_ID:
        try:
            uid = int(msg.text.split()[1])
            vip_users.add(uid)
            bot.send_message(uid, "✅ VIP activated")
        except:
            bot.reply_to(msg, "/vip 123456")

threading.Thread(target=scheduler).start()
bot.infinity_polling()

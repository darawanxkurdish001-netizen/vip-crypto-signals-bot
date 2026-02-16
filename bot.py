import telebot
import requests
import time
import random
from datetime import datetime

TOKEN = "8542082295:AAEZJMhyUojouhyIyUy6QyaZTh-4W5wbf3U"
bot = telebot.TeleBot(TOKEN)

# لیستی کوینەکان
coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data["price"])

def generate_signal():
    symbol = random.choice(coins)
    price = get_price(symbol)

    direction = random.choice(["BUY 🟢", "SELL 🔴"])
    tp = round(price * 1.02, 2)
    sl = round(price * 0.98, 2)

    signal = f"""
🚀 VIP CRYPTO SIGNAL 🚀
Coin: {symbol}
Direction: {direction}
Entry: {price}
Take Profit: {tp}
Stop Loss: {sl}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return signal

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to VIP Crypto Signals Bot 🔥")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal = generate_signal()
    bot.send_message(message.chat.id, signal)

print("Bot is running...")
bot.infinity_polling()

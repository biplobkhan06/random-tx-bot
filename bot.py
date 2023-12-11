import telebot
import json
import random
import requests
import time
import logging
from threading import Thread

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your bot token here
TOKEN = "here bot token"

# Create a bot instance
bot = telebot.TeleBot(TOKEN)

min_with = 100
max_with = 10000
post_channel = -1002049081909 # here you can add @username

# Global variables for withdraw and miner states
withdraw_state = False
miner_state = False

# Load names and hashes from JSON files
with open('names.json', 'r') as names_file, open('hashes.json', 'r') as hashes_file:
    names = json.load(names_file)
    hashes = json.load(hashes_file)

def random_names():
    return random.choice(names)

def random_hash():
    return random.choice(hashes)

# Function to fetch exchange rate
def get_exchange_rate(amount):
    exchange_rate_url = 'https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd'
    response = requests.get(exchange_rate_url)
    data = response.json()
    usd_amount = data['tether']['usd'] * amount
    return usd_amount

def withdraw_amount(minimum_withdraw, maximum_withdraw):
    return round(random.uniform(minimum_withdraw, maximum_withdraw), 2)

def get_random_miner(name, tx):
    miners = [
        {'title': '🔥 #V1 MINER PURCHASE 🔥', 'amount': '9.00000 USDT', 'in_usd': '9.00 $'},
        {'title': '🔥 #V2 MINER PURCHASE 🔥', 'amount': '15.00000 USDT', 'in_usd': '15.00 $'},
        {'title': '🔥 #V3 MINER PURCHASE 🔥', 'amount': '25.00000 USDT', 'in_usd': '25.00 $'},
        {'title': '🔥 #V4 MINER PURCHASE 🔥', 'amount': '90.00000 USDT', 'in_usd': '90.00 $'},
        {'title': '🔥 #V5 MINER PURCHASE 🔥', 'amount': '125.00000 USDT', 'in_usd': '125.00 $'},
    ]
    
    random_miner = random.choice(miners)
    return f"""
<b>{random_miner['title']}</b>

<b>✅</b> <code>Active</code>
<b>🆔 {name}</b>
<b>🏦</b> <i>{random_miner['amount']}</i> ~ <code>{random_miner['in_usd']}</code>
 
<b>Blockchain TXID:</b>
{tx}
 
<b>🎁 JOIN ~@CRYPTOGPUMININGBOT</b>
"""

# Define the /start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Welcome! Type /withdraw to start withdrawal, /miner to start mining.")

# Define the /withdraw command handler
@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    global withdraw_state
    user_id = message.from_user.id
    withdraw_state = True

    def post_random_withdraw():
        while withdraw_state:
            amount = withdraw_amount(min_with, max_with)
            in_usd = get_exchange_rate(amount)
            hash_link = f"<a href='https://tronscan.org/#/blockchain/transaction/{random_hash()}'>{random_hash()}</a>"

            text = f"""<b>✳️ NEW WITHDRAW SENT</b>

<b>{random_names()}</b> Has Received Withdraw Of <b>${amount:.2f} USDT ~ ${in_usd:.2f}</b> 

<b>⛓ TXID ID :</b> {hash_link}

<b>🔥 JOIN</b> ~ @USDTLEGITMININGBOT"""

            bot.send_message(post_channel, text, parse_mode="HTML", disable_web_page_preview=True)
            time.sleep(random.randint(60, 300))  # Sleep for 1 to 5 minutes

    withdraw_thread = Thread(target=post_random_withdraw)
    withdraw_thread.start()
    bot.reply_to(message, "Withdraw initiated. Type /stop_withdraw to stop.")

# Define the /stop_withdraw command handler
@bot.message_handler(commands=['stop_withdraw'])
def stop_withdraw(message):
    global withdraw_state
    withdraw_state = False
    bot.reply_to(message, "Withdrawal stopped.")

# Define the /miner command handler
@bot.message_handler(commands=['miner'])
def miner(message):
    global miner_state
    miner_state = True
    user_id = message.from_user.id
    name = random_names()
    tx = f"<a href='https://tronscan.org/#/blockchain/transaction/{random_hash()}'>{random_hash()}</a>"

    def post_random_miner():
        while miner_state:
            random_miner_text = get_random_miner(name, tx)
            bot.send_message(post_channel, random_miner_text, parse_mode="HTML", disable_web_page_preview=True)
            time.sleep(random.randint(60, 300))  # Sleep for 1 to 5 minutes

    miner_thread = Thread(target=post_random_miner)
    miner_thread.start()
    bot.reply_to(message, "Miner initiated. Type /stop_miner to stop.")

# Define the /stop_miner command handler
@bot.message_handler(commands=['stop_miner'])
def stop_miner(message):
    global miner_state
    miner_state = False
    bot.reply_to(message, "Miner stopped.")

if __name__ == '__main__':
    while True:
        try:
            print("bot is running")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot polling failed: {e}")
            bot.send_message(5337150824, f"Bot polling failed: {e}")
            time.sleep(10)

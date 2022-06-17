from datetime import datetime, timedelta
from FTXAPI import FtxClient
from time import sleep
from dotenv import load_dotenv
import os

from job_queue import JobQueue
from job import Jobs
from job_item import Job_Item
from telegrambot import TelegramBot
from trading_functions import *
import firebaseconfig as firebase

load_dotenv()

TOKEN = os.getenv('telegramToken')

FTX_API_KEY = os.getenv('FtxApiKey')
FTX_API_SECRET = os.getenv('FtxApiSecret')


def initialisation():
    return TelegramBot(TOKEN)
    
def main():
    time = datetime.now()
    coin_count = 0
    num_coins = len(coins)
    while True:
        try:
            result = bot.TelebotPoll(10)
            for input in result:
                message = input['message']
                chat_id = input['chat_id']
                name = input['first_name']
                print(input)
                pending_job = None
                
                if (message == '/start'):
                    if (chat_id not in bot.chatids):
                        print(f'Starting new session for {chat_id}')
                        bot.chatids.update({chat_id : name})
                    
                    pending_job = Job_Item(chat_id, message, Jobs.START)

                elif (message.startswith('/long_trade') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.LONGTRADE, current_coin)

                elif (message.startswith('/short_trade') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.SHORTTRADE, current_coin)
                    print("short trade job item created")
                
                elif (message == '/no_trade' and chat_id in bot.auth_users):
                    pending_job = Job_Item(chat_id, message, Jobs.NO_TRADE)

                elif (message == '/logout' and chat_id in bot.auth_users):
                    pending_job = Job_Item(chat_id, message, Jobs.LOGOUT)

                elif job_queue.is_valid_input(chat_id):
                    pending_job = Job_Item(chat_id, message, Jobs.USERNAME)
                
                else:
                    bot.sendText(
                        "Invalid input, press /start to use CoinValet or use another valid prompt",
                        chat_id
                    )
                    continue

                if pending_job:
                    job_queue.push_job(pending_job)
                    pending_job = None

            job_queue.execute()
            current_time = datetime.now()
        
            if (current_time > (time + timedelta(minutes= trade_freq)) or coin_count != 0):
                coin = coins[coin_count]
                
                if coin_count >= (num_coins - 1):
                    coin_count = 0
                else:
                    coin_count+= 1

                time = current_time
                trading_algo(bot, coin, interval, ftx)
                
        except:
            print("ERROR in Main Loop")
            sleep(10)
            pass



if __name__ == '__main__':
    coins = ['RUNE-PERP', 'BTC-PERP']
    interval = '1h'

    site = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    
    """Initialise the Telegram bot"""
    bot = initialisation()

    """Initialise connection with FTX"""
    ftx = FtxClient(api_key= FTX_API_KEY, api_secret= FTX_API_SECRET)

    """Initialise Firebase database and authentication"""
    user_db = firebase.db
    user_auth = firebase.auth

    """Initialise the Job Queue"""
    job_queue = JobQueue(bot, user_db, user_auth)

    """Trade suggestion frequency (in minutes)"""
    trade_freq = 0.2

    main()


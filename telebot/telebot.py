import os
import firebaseconfig as firebase
from datetime import datetime, timedelta
from dotenv import load_dotenv
from FTXAPI import FtxClient
from time import sleep

from job import Jobs
from job_item import Job_Item
from job_queue import JobQueue
from telegrambot import TelegramBot
from trading_functions import *
from portfolio_metrics import *

"""Handle API KEYS"""
load_dotenv()

TOKEN = os.getenv('telegramToken')

FTX_API_KEY = os.getenv('FtxApiKey')
FTX_API_SECRET = os.getenv('FtxApiSecret')

"""Constants"""
COIN_PRICE_UPDATE_FREQ = 30
PORTFOLIO_METRICS_UPDATE_FREQ = 30
TRADE_SUGGESTION_FREQ = 1


"""Initialise Telegram Bot with Token"""
def initialisation():
    return TelegramBot(TOKEN)


def main():
    trade_freq_time = datetime.now()
    coin_update_time = datetime.now()
    metrics_update_time = datetime.now()
    coin_count = 0
    num_coins = len(coins)
    while True:
        try:
            result = bot.TelebotPoll(10)
            for input in result:
                message = input['message']
                chat_id = input['chat_id']
                name = input['first_name']
                pending_job = None
                
                if (message == '/start'):
                    
                    if (chat_id in bot.sleep):
                        bot.sleep.remove(chat_id)

                    if (chat_id in bot.auth_users):
                        del bot.auth_users[chat_id]
                    
                    pending_job = Job_Item(chat_id, message, Jobs.START)

                elif (message.startswith('/long_trade') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.LONGTRADE, current_coin)

                elif (message.startswith('/short_trade') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.SHORTTRADE, current_coin)

                elif (message.startswith('/close_long') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.CLOSELONG, current_coin)
                    
                elif (message.startswith('/close_short') and chat_id in bot.auth_users):
                    current_coin = message.split('_')[2]
                    pending_job = Job_Item(chat_id, message, Jobs.CLOSESHORT, current_coin)

                elif (message == '/sleep' and chat_id in bot.auth_users):
                    pending_job = Job_Item(chat_id, message, Jobs.SLEEP)

                elif (message == '/listen' and chat_id in bot.auth_users):
                    pending_job = Job_Item(chat_id, message, Jobs.LISTEN)

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
                
                """Adds valid pending jobs to the job queue"""
                if pending_job:
                    job_queue.push_job(pending_job)
                    pending_job = None

            """Executes all pending jobs in job queue"""
            job_queue.execute()
    
            current_time = datetime.now()
        
            """Executes the trading algorithm to get trade suggestions every time interval
            predifined by TRADE_SUGGESTION_FREQ"""
            if (current_time > (trade_freq_time + timedelta(minutes= TRADE_SUGGESTION_FREQ)) or coin_count != 0):
                coin = coins[coin_count]
                
                if coin_count >= (num_coins - 1):
                    coin_count = 0
                else:
                    coin_count+= 1

                trade_freq_time = current_time
                trading_algo(bot, coin, interval, ftx)
        
            """Updates the coin prices in the database every time interval 
            predefined by COIN_PRICE_UPDATE_FREQUENCY"""
            if (current_time > (coin_update_time + timedelta(minutes= COIN_PRICE_UPDATE_FREQ))):
                print('Running Coin Price Update')
                coin_update_time = current_time
                price_update(bot, coins, ftx)
        
            """Updates the portfolio metrics of every user in the database every time interval
            predefined by PORTFOLIO_METRICS_UPDATE_FREQ"""
            if (current_time > (metrics_update_time + timedelta(minutes= PORTFOLIO_METRICS_UPDATE_FREQ))):
                metrics_update_time = current_time
                update_metrics(bot, coins, ftx, 'adi@gmail.com')
                
        except:
            print("ERROR in Main Loop")
            sleep(10)
            pass



if __name__ == '__main__':
    coins = ['RUNE-PERP', 'BTC-PERP', 'ETH-PERP', 'SOL-PERP']
    interval = '1h'

    site = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    
    """Initialise the Telegram bot"""
    bot = initialisation()

    """Initialise connection with FTX"""
    ftx = FtxClient(api_key= FTX_API_KEY, api_secret= FTX_API_SECRET)

    """Initialise Firebase authentication"""
    user_auth = firebase.auth

    """Initialise the Job Queue"""
    job_queue = JobQueue(bot, user_auth)

    main()


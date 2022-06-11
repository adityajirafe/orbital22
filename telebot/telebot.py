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
    
def shortform(coin: str):
    count = 0
    for letter in coin:
        if letter == "-":
            break
        else:
            count+= 1
    return coin[0:count]

def main(coins):
    
    while True:
        try:
            result = bot.TelebotPoll(10)
            for input in result:
                message = input['message']
                chat_id = input['chat_id']
                name = input['first_name']
                print(input)
                pending_job = None
                
                coin = coins[0]
                shortened_coin = shortform(coin)
                if (message == '/start'):
                    if (chat_id not in bot.chatids):
                        print(f'Starting new session for {chat_id}')
                        bot.chatids.update({chat_id : name})
                    
                    pending_job = Job_Item(chat_id, message, Jobs.START)
                    
                # elif bot.initialsed == True:
                
                elif (message == f'/long_trade_{shortened_coin}'):
                    pending_job = Job_Item(chat_id, message, Jobs.LONGTRADE, coin)

                elif (message == f'/short_trade_{shortened_coin}'):
                    pending_job = Job_Item(chat_id, message, Jobs.SHORTTRADE, coin)
                    print("short trade job item created")
                
                elif (message == '/no_trade'):
                    pending_job = Job_Item(chat_id, message, Jobs.NO_TRADE)

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
            trading_algo(bot, coins, interval)
        except:
            print("ERROR in Main Loop")
            sleep(10)
            pass



if __name__ == '__main__':
    coins = ['RUNE-PERP']
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

    main(coins)


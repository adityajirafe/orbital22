from mimetypes import init
import os
import firebaseconfig as firebase
from datetime import datetime, timedelta
from dotenv import load_dotenv
from FTXAPI import FtxClient
from time import sleep
import unittest
from unittest.mock import Mock, patch
import io

from firebaseconfig import login
from telebot import initialisation, main
from job import Jobs
from job_item import Job_Item
from job_queue import JobQueue
from telegrambot import TelegramBot
from trading_functions import *
from portfolio_metrics import *
from functions import *

load_dotenv()

TOKEN = "1909563028:AAFE7AUF3bq0o100YJWs_FP1UF_obNp6nDA"
CHAT_ID = "127483518"
FTX_API_KEY = os.getenv('ReadOnlyFtxApiKey')
FTX_API_SECRET = os.getenv('ReadOnlyFtxApiSecret')

"""Initialise connection with FTX"""
ftx = FtxClient(api_key= FTX_API_KEY, api_secret= FTX_API_SECRET)

coins = []
coins_and_qty = {'RUNE-PERP': 1, 'BTC-PERP': 0.001, 'ETH-PERP': 0.001, 'SOL-PERP': 0.1}
for coin in coins_and_qty:
    coins.append(coin)
interval = '1h'

"""Initialise the Telegram bot"""
bot = initialisation(TOKEN, coins_and_qty, coins, ftx)

"""Initialise Firebase authentication"""
user_auth = firebase.auth

"""Initialise the Job Queue"""
job_queue = JobQueue(bot, user_auth)

class Test(unittest.TestCase):    
    def test_correct_login(self):
        self.assertTrue(login("test@gmail.com", "123456", user_auth))
        print("test correct login details done")

    def test_incorrect_pwd(self):
        self.assertFalse(login("test@gmail.com", "123456789", user_auth))
        print("test incorrect password done")

    def test_incorrect_email(self):
        self.assertFalse(login("testing@gmail.com", "123456", user_auth))
        print("test incorrect email")

    def test_getData(self):
        self.assertIsInstance(getData(coins[0], interval, ftx), pd.DataFrame)
        print("test get data done")

    def bot_send_Text(self, message, chat_id):
        try:
            bot.sendText(message, chat_id)
            return True
        except:
            print("error in sending text")
            return False
    
    def test_sendText(self):
        self.assertTrue(self.bot_send_Text("testing send text", CHAT_ID))
        print("test send text done")
    
    def bot_send_image(self, directory, chat_id):
        try:
            bot.sendImage(directory, chat_id)
            return True
        except:
            print("error in sending text")
            return False

    def test_sendImage(self):
        self.assertTrue(self.bot_send_image("telebot/graph.png", CHAT_ID))
        print("test send image done")

    def test_detect_trade(self):
        self.assertIsInstance(detect_trade(coins[0], interval, ftx), dict)
        print("test detect trade done")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_notrade(self, job_item, expected_output, mock_stdout):
        handle_no_trade(job_item, bot)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_no_trade(self):
        # The actual test
        job_item = Job_Item(CHAT_ID, "/no_trade_RUNE", Jobs.NOTRADE, "RUNE")
        self.assert_notrade(job_item, 'handled no trade\n')
        print("test no trade done")
        

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_long_trade(self, bot, margin, expected_output, mock_stdout):
        job_item = Job_Item(CHAT_ID, "/long_trade_RUNE", Jobs.LONGTRADE, "RUNE")
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        handle_long_trade(job_item, bot, margin)
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    def test_long_trade(self):
        # The actual test
        margin = 1
        self.assert_long_trade(bot, margin, 'RUNE price updated.\n/long_trade_RUNE\n')
        print("test long trade done")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_open_short_with_long_pos(self, bot, margin, expected_output, mock_stdout):
        job_item = Job_Item(CHAT_ID, "/short_trade_RUNE", Jobs.SHORTTRADE, "RUNE")
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        handle_short_trade(job_item, bot, margin)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_open_short_with_long_pos(self):
        # The actual test
        margin = 1
        self.assert_open_short_with_long_pos(bot, margin, 'RUNE long opened has been closed\nstart pulling prices\nbest position done\nworst position done\nall time done\ndailyPnL done\ndailyPnLPercent done\nytdPnL done\ndaily done\nupdated metrics after trade closed by test@gmail.com\n')
        print("test open short when there is an existing long position done")

if __name__ == '__main__':
    unittest.main()
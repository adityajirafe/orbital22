import os

from charset_normalizer import detect
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

TOKEN = os.getenv('testingTelegramToken')
CHAT_ID = os.getenv('testingChatId')
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
    """Test whether the login credentials are correct""" 
    def test_correct_login(self):
        self.assertTrue(login("test@gmail.com", "123456", user_auth))

    """Test whether the password is incorrect"""
    def test_incorrect_pwd(self):
        self.assertFalse(login("test@gmail.com", "123456789", user_auth))

    """Test whether the email is incorrect"""
    def test_incorrect_email(self):
        self.assertFalse(login("testing@gmail.com", "123456", user_auth))
        
    """Test if the function is able to get data from FTX"""
    def test_getData(self):
        self.assertIsInstance(getData(coins[0], interval, ftx), pd.DataFrame)

    def send_text_helper(self, message, chat_id):
        try:
            bot.sendText(message, chat_id)
            return True
        except:
            print("error in sending text")
            return False
    
    """Test if the bot is able to send a text to a user"""
    def test_sendText(self):
        self.assertTrue(self.send_text_helper("testing send text", CHAT_ID))
    
    def send_image_helper(self, directory, chat_id):
        try:
            bot.sendImage(directory, chat_id)
            return True
        except:
            print("error in sending text")
            return False

    """Test if the bot is able to send an image to a user"""
    def test_sendImage(self):
        self.assertTrue(self.send_image_helper("telebot/graph.png", CHAT_ID))

    """Test if the bot is able to detect a trade"""
    def test_detect_trade(self):
        self.assertIsInstance(detect_trade(coins[0], interval, ftx), dict)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_notrade(self, expected_output, mock_stdout):
        job_item = Job_Item(CHAT_ID, "/no_trade_RUNE", Jobs.NOTRADE, "RUNE")
        job_queue.push_job(job_item)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    """Test if the bot is able to handle no trade commands"""
    def test_no_trade(self):
        # The actual test
        self.assert_notrade('handled no trade\n')     

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_trade(self, type, bot, margin, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        if type == 'LONG':
            job_item = Job_Item(CHAT_ID, "/long_trade_RUNE", Jobs.LONGTRADE, "RUNE", type)
        elif type == 'SHORT':
            job_item = Job_Item(CHAT_ID, "/short_trade_RUNE", Jobs.SHORTTRADE, "RUNE", type)
        job_queue.push_job(job_item)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)
        
    """Test if the bot is able to open a position based on the detected trade"""
    def test_trade(self):
        # The actual test
        margin = 1
        type = detect_trade(coins[0], interval, ftx)['type']
        if type == 'LONG':
            self.assert_trade('LONG', bot, margin, '/long_trade_RUNE\n')
        elif type == 'SHORT':
            self.assert_trade('SHORT', bot, margin, '/short_trade_RUNE\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_trade_with_opposite_pos(self, opened_trade, bot, margin, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        if opened_trade == 'LONG':
            job_item = Job_Item(CHAT_ID, "/short_trade_RUNE", Jobs.SHORTTRADE, "RUNE", "SHORT")
        elif opened_trade == 'SHORT':
            job_item = Job_Item(CHAT_ID, "/long_trade_RUNE", Jobs.LONGTRADE, "RUNE", "LONG")

        job_queue.push_job(job_item)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    """Test if the bot is able to close a position when the command to open a position in the opposite direction is given"""
    def test_close_pos_with_opened_opposite_pos(self):
        # The actual test
        margin = 1
        type = get_positions("test@gmail.com", "RUNE")[0][1]['name']
        if type == 'long':
            self.assert_trade_with_opposite_pos('LONG', bot, margin, 'RUNE long opened has been closed\nstart pulling prices\nmetrics updated\nupdated metrics after trade closed by test@gmail.com\n')
        elif type == 'short':
            self.assert_trade_with_opposite_pos('SHORT', bot, margin, 'RUNE short opened has been closed\nstart pulling prices\nmetrics updated\nupdated metrics after trade closed by test@gmail.com\n')
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_trade_opposite_favour(self, bot, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        job_item_1 = Job_Item(CHAT_ID, "/short_trade_RUNE", Jobs.SHORTTRADE, "RUNE", "LONG")
        job_item_2 = Job_Item(CHAT_ID, "/long_trade_RUNE", Jobs.LONGTRADE, "RUNE", "SHORT")
        job_queue.push_job(job_item_1)
        job_queue.push_job(job_item_2)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    '''Test if the trade will not be taken because the favoured trade is opposite of the command'''
    def test_trade_opposite_favour(self):
        self.assert_trade_opposite_favour(bot, "Cannot take short trade when favoured trade is long\nCannot take long trade when favoured trade is short\n")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_close_empty_position(self, bot, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        job_item_1 = Job_Item(CHAT_ID, "/close_short_SOL", Jobs.CLOSESHORT, "SOL")
        job_item_2 = Job_Item(CHAT_ID, "/close_long_SOL", Jobs.CLOSELONG, "SOL")
        job_queue.push_job(job_item_1)
        job_queue.push_job(job_item_2)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    '''Test if the bot is able to detect that there are no open positions that the user is trying to close'''
    def test_close_empty_position(self):
        self.assert_close_empty_position(bot, "No SOL positions opened\nNo SOL positions opened\n")
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_close_empty_long_position(self, bot, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        bot.update_coin_prices("ETH", "1200")
        job_item_1 = Job_Item(CHAT_ID, "/close_long_ETH", Jobs.CLOSELONG, "ETH")
        job_queue.push_job(job_item_1)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_close_empty_long_position(self):
        self.assert_close_empty_long_position(bot, "No open ETH long positions\n")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_invalid_coin(self, bot, expected_output, mock_stdout):
        bot.auth_users = {CHAT_ID: ftx}
        bot.chatids = {CHAT_ID: "test@gmail.com"}
        job_item_1 = Job_Item(CHAT_ID, "/short_trade_DOGE", Jobs.SHORTTRADE, "DOGE")
        job_item_2 = Job_Item(CHAT_ID, "/long_trade_DOGE", Jobs.LONGTRADE, "DOGE")
        job_item_3 = Job_Item(CHAT_ID, "/close_short_DOGE", Jobs.CLOSESHORT, "DOGE")
        job_item_4 = Job_Item(CHAT_ID, "/close_long_DOGE", Jobs.CLOSELONG, "DOGE")
        job_queue.push_job(job_item_1)
        job_queue.push_job(job_item_2)
        job_queue.push_job(job_item_3)
        job_queue.push_job(job_item_4)
        job_queue.execute()
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    '''Test if the coin in the command is one of the coins traded'''
    def test_invalid_coin(self):
        self.assert_invalid_coin(bot, "invalid coin\ninvalid coin\ninvalid coin\ninvalid coin\n")

if __name__ == '__main__':
    unittest.main()
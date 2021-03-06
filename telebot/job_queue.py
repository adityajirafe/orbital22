import os
from firebaseconfig import login
from FTXAPI import FtxClient
from dotenv import load_dotenv
from datetime import timedelta, datetime

from job import Jobs
from functions import *
from portfolio_metrics import *

load_dotenv()

class JobQueue:
    def __init__(self, bot, auth):
        """Store the Telebot Object"""
        self.bot = bot
        """Store Authentication object"""
        self.auth = auth
        """Store jobs pushed into job queue"""
        self.queue = []
        """Store users currently being served"""
        self.waiting = {}
        """Set the default margin used to execute trades"""
        self.margin = 1
        """Set the default login waiting time to be 30seconds"""
        self.waiting_time = 30


    """Push jobs into job queue"""
    def push_job(self, job_item):
        self.queue.append(job_item)


    """Checks whether the input is email or password"""
    def is_valid_input(self, chat_id):
        if chat_id in self.waiting:
            return True
        return False


    """Execute jobs in job queue"""
    def execute(self):
        try:
            """Handle users who are crrently being served first"""
            self.check_waiting()

            while self.queue:
                job_item = self.queue[0]
                if job_item.job is Jobs.START:
                    handle_start(job_item, self.bot)
                    time = datetime.now() + timedelta(minutes= 480)
                    waiting_time = time + timedelta(seconds=self.waiting_time)
                    self.waiting.update({f'{job_item.chat_id}': {'waiting_time': waiting_time, 'job': Jobs.USERNAME}})
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.LONGTRADE:
                    handle_long_trade(job_item, self.bot, self.margin, job_item.favoured_trade)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.SHORTTRADE:
                    handle_short_trade(job_item, self.bot, self.margin, job_item.favoured_trade)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.CLOSELONG:
                    chat_id = job_item.chat_id
                    email = self.bot.chatids[job_item.chat_id]
                    coin = job_item.coin
                    
                    if coin + "-PERP" not in self.bot.coins:
                        self.bot.sendText(f'Invalid coin, we only trade\n{self.bot.coins[0]}\n{self.bot.coins[1]}\n{self.bot.coins[2]}\n{self.bot.coins[3]}', chat_id)
                        print('invalid coin')
                    else:
                        positions = get_positions(email, coin)
                        if positions == []:
                            self.bot.sendText(f'No {coin} positions opened', chat_id)
                            print(f'No {coin} positions opened')
                        else:
                            handle_close_trade(positions, 'short', email, self.bot, chat_id)
                    self.queue.remove(job_item)
                
                elif job_item.job is Jobs.CLOSESHORT:
                    chat_id = job_item.chat_id
                    email = self.bot.chatids[job_item.chat_id]
                    coin = job_item.coin
                    if coin + "-PERP" not in self.bot.coins:
                        self.bot.sendText(f'Invalid coin, we only trade\n{self.bot.coins[0]}\n{self.bot.coins[1]}\n{self.bot.coins[2]}\n{self.bot.coins[3]}', chat_id)
                        print('invalid coin')
                    else:
                        positions = get_positions(email, coin)
                        if positions == []:
                            self.bot.sendText(f'No {coin} positions opened', chat_id)
                            print(f'No {coin} positions opened')
                        else:
                            handle_close_trade(positions, 'long', email, self.bot, chat_id)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.NOTRADE:
                    handle_no_trade(job_item, self.bot)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.LOGOUT:
                    handle_logout(job_item, self.bot)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.SLEEP:
                    handle_sleep(job_item, self.bot)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.LISTEN:
                    handle_listen(job_item, self.bot)
                    self.queue.remove(job_item)

                elif job_item.job is Jobs.BALANCE:
                    handle_balance(job_item, self.bot)
                    self.queue.remove(job_item)
                    
                else:
                    break
        except:
            print("No more jobs") #Debugging statement
        finally:
            return

    """Handles input from users currently being served"""
    def check_waiting(self):
        
        if not self.waiting:
            return
        for chat_id in self.waiting:
            if self.waiting[chat_id]['waiting_time'] < datetime.now() + timedelta(minutes= 480):
                print('timeout')
                self.bot.sendText(
                    "Login Timeout. Press /start to restart bot",
                    chat_id
                )
                del self.waiting[chat_id]
                return
                    
        for job_item in self.queue:
            chat_id = job_item.chat_id

            if chat_id in self.waiting:
                
                job = self.waiting[chat_id]['job']

                if job_item.message == '/start':
                    self.bot.sendText(
                        "Invalid Input. Press /start to restart bot",
                        chat_id
                    )
                    del self.waiting[chat_id]
                    self.queue.remove(job_item)
                    return
                
                if job is Jobs.USERNAME:
                    time = datetime.now() + timedelta(minutes= 480)
                    waiting_time = time + timedelta(seconds=self.waiting_time)
                    username = handle_username(job_item, self.bot)
                    self.waiting.update(
                        {chat_id: {'waiting_time': waiting_time, 'job': Jobs.PASSWORD, 'username': username}}
                    )
                    self.queue.remove(job_item)
                    return

                elif job is Jobs.PASSWORD:
                    password = handle_password(job_item, self.bot)
                    email = self.waiting[chat_id]['username']
                    if (login(email, password, self.auth)):
                        
                        FTX_API_KEY = os.getenv('FtxApiKey')
                        FTX_API_SECRET = os.getenv('FtxApiSecret')
                        ftxobj = FtxClient(api_key= FTX_API_KEY, api_secret= FTX_API_SECRET)
                        
                        """Mark user as aunthenticated so they can receive trade suggestions"""
                        self.bot.authenticate_user(chat_id, ftxobj)
                        self.bot.store_email(chat_id, email)
                        self.bot.sendText(
                            "Log in successful! \nYou will now begin to receive trade suggestions",
                            chat_id
                        )
                        
                    else: 
                        self.bot.sendText(
                            "User not found. Press /start to restart bot\nNew users head to the CoinValet App to sign up!", 
                            chat_id
                        )

                    del self.waiting[chat_id]
                    self.queue.remove(job_item)
                    email = self.bot.chatids[chat_id]
                    print(f"coins: {self.bot.coins}")
                    update_metrics(self.bot, self.bot.coins, self.bot.master_ftxobj, email)
                    print('updated metrics after user authenticated')
                    return
                else:
                    continue
        print("Pending Job") #Debugging Statement
        return 
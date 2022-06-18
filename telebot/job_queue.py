from job import Jobs
from functions import *

from firebaseconfig import login
# temporary import ftxapi until we figure out how to pull ftxobj from firestore
from FTXAPI import FtxClient
from dotenv import load_dotenv
import os
load_dotenv()

# users = []

class JobQueue:
    def __init__(self, bot, db, auth):
        self.bot = bot
        self.db = db
        self.auth = auth
        self.queue = []
        self.waiting = {}
        # Default margin for trades 
        self.margin = 1

    def push_job(self, job_item):
        self.queue.append(job_item)

    def is_valid_input(self, chat_id):
        if chat_id in self.waiting:
            return True
        return False

    def execute(self):
        #for i in self.queue:
            #print(f"Task: {i.message}")
        try:
            self.check_waiting()
            while self.queue:
                job_item = self.queue[0]
                if job_item.job is Jobs.START:
                    handle_start(job_item, self.bot)
                    self.waiting.update({f'{job_item.chat_id}': {'job': Jobs.USERNAME}})
                    self.queue.remove(job_item)
                elif job_item.job is Jobs.LONGTRADE:
                    handle_long_trade(job_item, self.bot, self.margin)
                    self.queue.remove(job_item)
                elif job_item.job is Jobs.SHORTTRADE:
                    handle_short_trade(job_item, self.bot, self.margin)
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
                else:
                    break
        except:
            print("No more jobs") 
        finally:
            return

    def check_waiting(self):
        if not self.waiting:
            return
        for job_item in self.queue:
            chat_id = job_item.chat_id
            if chat_id in self.waiting:
                job = self.waiting[chat_id]['job']
                if job_item.message == '/start':
                    self.bot.sendText("Invalid Input. Press /start to restart bot", chat_id)
                    del self.waiting[chat_id]
                    self.queue.remove(job_item)
                    return
                if job is Jobs.USERNAME:
                    username = handle_username(job_item, self.bot)
                    self.waiting.update({chat_id: {'job': Jobs.PASSWORD, 'username': username}})
                    self.queue.remove(job_item)
                    return
                elif job is Jobs.PASSWORD:
                    password = handle_password(job_item, self.bot)
                    # users.append([self.waiting[chat_id]['username'], password])
                    email = self.waiting[chat_id]['username']
                    if (login(email, password, self.auth)):
                        
                        # need to call/create the ftx object here using the email/username/chatid as the key, 
                        # and the ftx info as the value, from firestore
                        FTX_API_KEY = os.getenv('FtxApiKey')
                        FTX_API_SECRET = os.getenv('FtxApiSecret')
                        ftxobj = FtxClient(api_key= FTX_API_KEY, api_secret= FTX_API_SECRET)
                        
                        # Mark user as aunthenticated so they can receive trade suggestions
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

                    # print(f"THE USERS ARE: {users}")
                    return
                else:
                    continue
        print("Pending Job")
        return 
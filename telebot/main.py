from FTXAPI import FtxClient
from dbhelper import DBHelper
from telegrambot import TelegramBot
import talib as ta
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report #F-Score
import requests
from datetime import timedelta, datetime
from time import sleep
import telebot
import mplfinance as fplt

# create an instance of the database
db = DBHelper()
db.setup()
# input your own api key and api secret
api_key = ""
api_secret=""
ftx = FtxClient(api_key= api_key, api_secret= api_secret)
token = "5393382907:AAEL6kg6HYwAWD90OKTYpV98RU18eAlgtkM"

coin = 'BTC-PERP'

def handle_user(t: TelegramBot):
    t.sendText("Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your username")
    username = t.TelebotPoll(60)
    while (username == '' or username == '/start'):
        t.sendText("Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your username")
        username = t.TelebotPoll(60)
    t.sendText("Please input your password")
    password = t.TelebotPoll(60)
    while (password == '' or password == '/start'):
        t.sendText("Please input your password")
        password = t.TelebotPoll(60)
    
    user = (t.chatid, username, password, api_key, api_secret)
    print(user)

    list_of_users = db.get_users_cred()
    if t.chatid in list_of_users:
        db.delete_user(t.chatid)
        db.add_user(user)
        t.sendText(f"Hello {username}")
        trade(t)
    else:
        db.add_user(user)
        t.sendText("user not found\n\nuser successfully added")
        trade(t)

def checkTrade(margin: float) -> bool:
    s = ftx.get_balances()
    if (s == []):
        return False
    balances = pd.data(s)
    lst = balances.coin.tolist()
    if ("USD" in lst):
        index = lst.index("USD")
        return balances.free[index] > margin
    return False

def getData(coin: str, time: str):
    # getting the data frame
    df = ftx.get_market_data(coin, time)
    df = ftx.parse_ftx_response(df.json())
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)

    # adding the RSI column
    df['RSI'] = ta.RSI(df['close'], timeperiod = 9)

    #adding the 50 day EMA
    df['50EMA'] = ta.EMA(df['close'], timeperiod = 50)

    #adding the 10 day EMA
    df['10EMA'] = ta.EMA(df['close'], timeperiod = 10)
    return df

def trade(t: TelegramBot):
    position = 0
    while True:
        df = getData(coin, '1h')

        #plotting the graph and saving it
        ap2 = [fplt.make_addplot(df['50EMA'], color='b', panel= 1), 
                fplt.make_addplot(df['10EMA'], color='y', panel= 1),
                fplt.make_addplot(df['RSI'], color='#6a0dad', panel= 2)]
        fplt.plot(
                df,
                type='candle',
                style= 'charles',
                title= coin + ' chart',
                ylabel='Price ($)',
                main_panel= 1,
                addplot= ap2,
                savefig= "graph.png"
        )
        i = len(df) - 1
        t.sendText(f"BTC price is {df['close'][i]}")
        t.sendImage("graph.png")
        
        if (df['10EMA'][i] > df['50EMA'][i] and position == 0):
            t.sendText("time to open LONG position\n\n/trade\n\n/no_trade")
            reply = t.TelebotPoll(30)
            if (reply == '/trade'):
                if (checkTrade(1)):
                    try:
                        price = df['close'][i]
                        ftx.place_order(market= coin, side= 'buy', price= str(price), type= 'limit', size= 0.001)
                        print(order["status"])
                        t.sendText(f"Trade has been taken\nat {price}")
                        position = 1
                    except:
                        t.sendText( "some other error occured")
                else:
                    t.sendText("not enough money to make the trade")

            else: 
                price = df['close'][i]
                t.sendText(f"Trade has NOT been taken\nat {price}")
                position = 0
        elif (df['10EMA'][i] < df['50EMA'][i] and position == 0):
            t.sendText("time to open SHORT position\n\n/trade\n\n/no_trade")            
            reply = t.TelebotPoll(30)
            if (reply == '/trade'):
                if (checkTrade(1)):
                    try:
                        price = df['close'][i]
                        ftx.place_order(market= coin, side= 'sell', price= str(price), type= 'limit', size= 0.001)
                        print(order["status"])
                        t.sendText(f"Trade has been taken\nat {price}")
                        position = 2
                    except:
                        t.sendText("some other error occured")
                else:
                    t.sendText("not enough money bij")

            else: 
                price = df['close'][i]
                t.sendText(f"Trade has NOT been taken\nat {price}")
                position = 0
        elif (df['10EMA'][i] <= df['50EMA'][i] and position == 1):
            t.sendText(f"time to close LONG position\n\n/close\n\n/dont_close")
            reply = t.TelebotPoll(30)
            if (reply == '/close'):
                price = df['close'][i]
                t.sendText(f"Trade has been closed\nat {price}")
                position = 0
                ftx.place_order(market= coin, side= 'sell', price= str(price), type= 'limit', size= 0.001)
                print(order["status"])
            else: 
                price = df['close'][i]
                t.sendText(f"Trade has NOT been closed\nat {price}")
                position = 1
        elif (df['10EMA'][i] >= df['50EMA'][i] and position == 2):
            t.sendText("time to close SHORT position\n\n/close\n\n/dont_close")
            reply = t.TelebotPoll(30)
            if (reply == '/close'):
                price = df['close'][i]
                t.sendText(f"Trade has been closed\nat {price}")
                position = 0
                order = ftx.place_order(market= coin, side= 'buy', price= str(price), type= 'limit', size= 0.001)
                print(order["status"])
            else: 
                price = df['close'][i]
                t.sendText(f"Trade has NOT been closed\nat {price}")
                position = 2
        response = t.TelebotPoll(60)
        if (response == "/mybalance"):
            t.sendText(str(ftx.get_balances()))
        elif (response == "/logout"):            
            t.sendText('successfully logged out')
            break

def mainmain(chatid: str):
    t = TelegramBot(botToken= token, chatid= chatid, graphDirectory= "graph.png")
    if (t.TelebotPoll(10) == '/start'):
        handle_user(t)
    else: 
        t.sendText('please press /start to login to your CoinValet account')


# list_of_chatids= []

site = f'https://api.telegram.org/bot{token}/getUpdates'

while True:
    data = requests.get(site).json()  # reads data from the url getUpdates
    lastMsg = len(data['result']) - 1
    chatid = str(data['result'][lastMsg]['message']['from']['id'])

    # if chatid not in list_of_chatids:
    #     list_of_chatids.append(chatid)
    # print(list_of_chatids)
    mainmain(chatid)

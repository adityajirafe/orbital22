from sre_constants import SUCCESS
from FTXAPI import FtxClient
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

# input your own api key and api secret
ftx = FtxClient(api_key= "", api_secret="")

coin = 'BTC-PERP'

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

class telegrambot:
    def __init__(self, botToken, graphDirectory):
        assert botToken == str(botToken), 'Name has to be a string'
        assert graphDirectory == str(graphDirectory), 'Directory has to be a string'
        self.botToken = botToken
        self.graphDirectory = graphDirectory

    def TelebotPoll(self, waitTime):
        site = f'https://api.telegram.org/bot{self.botToken}/getUpdates'
        data = requests.get(site).json()  # reads data from the url getUpdates
        lastMsg = len(data['result']) - 1
        updateIdSave = data['result'][lastMsg]['update_id']
        decision = 'none'
        time = datetime.now()
        waitingTime = time + timedelta(seconds=waitTime)

        while True:
            try:
                data = requests.get(site).json()  # reads data from the url getUpdates
                lastMsg = len(data['result']) - 1
                updateId = data['result'][lastMsg]['update_id']
                if updateId != updateIdSave:  # compares update ID
                    try:
                        text = data['result'][lastMsg]['message']['text']  # reads what they have sent\
                        break
                    except:
                        pass
                if waitingTime < datetime.now():
                    text = 'null'
                    break
            except:
                pass
        requests.get(
            f'https://api.telegram.org/bot{self.botToken}/getUpdates?offset=' + str(updateId))
        return text

    def sendText(self, chatid, message):
        URL=f"https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={chatid}&text={message}"
        requests.get(URL)

    def sendGraph(self, chatid, graph):
        print(self.graphDirectory)
        try:
            print("inside try block")
            graph.write_image(self.graphDirectory)
            print("Graph written")
            return self.sendImage(chatid, self.graphDirectory)
        except:
            print("Failed to send Graph")

    def sendImage(self, chatid, directory):
        try:
            imgpath = {'photo': open(directory, 'rb')}
            requests.post(
                f'https://api.telegram.org/bot{self.botToken}/sendPhoto?chat_id={chatid}',
                files=imgpath)  # Sending Automated Image
            print("Image Sent")
        except:
            print("Failed to send Image")


token = "5393382907:AAEL6kg6HYwAWD90OKTYpV98RU18eAlgtkM"
t = telegrambot(botToken= token, graphDirectory= "graph.png")

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


site = f'https://api.telegram.org/bot{t.botToken}/getUpdates'
data = requests.get(site).json()  # reads data from the url getUpdates
#chatid = data['result'][0]['message']['from']['id']
chatid = '127483518'

t.sendText(chatid, "Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your username")
username = t.TelebotPoll(60)
while (username == 'null'):
    t.sendText(chatid, "Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your username")
    username = t.TelebotPoll(60)
t.sendText(chatid, username + "\nPlease input your password")
password = t.TelebotPoll(60)
while (password == 'null'):
    t.sendText(chatid, username + "\nPlease input your password")
    password = t.TelebotPoll(60)

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
    t.sendText(chatid, "BTC price")
    t.sendText(chatid, df['close'])
    t.sendImage(chatid, "graph.png")

    i = len(df) - 1
    if (df['10EMA'][i] > df['50EMA'][i] and position == 0):
        t.sendText(chatid, "time to open LONG position\n\n/trade\n\n/no_trade")
        reply = t.TelebotPoll(30)
        if (reply == '/trade'):
            if (checkTrade(1)):
                try:
                    price = df['close'][i]
                    ftx.place_order(market= coin, side= 'buy', price= str(price), type= 'limit', size= 0.001)
                    print(order["status"])
                    t.sendText(chatid, f"Trade has been taken\nat {price}")
                    position = 1
                except:
                    t.sendText(chatid, "some other error occured")
            else:
                t.sendText(chatid, "not enough money bij")

        else: 
            price = df['close'][i]
            t.sendText(chatid, f"Trade has NOT been taken\nat {price}")
            position = 0
    elif (df['10EMA'][i] < df['50EMA'][i] and position == 0):
        t.sendText(chatid, "time to open SHORT position\n\n/trade\n\n/no_trade")            
        reply = t.TelebotPoll(30)
        if (reply == '/trade'):
            if (checkTrade(1)):
                try:
                    price = df['close'][i]
                    ftx.place_order(market= coin, side= 'sell', price= str(price), type= 'limit', size= 0.001)
                    print(order["status"])
                    t.sendText(chatid, f"Trade has been taken\nat {price}")
                    position = 2
                except:
                    t.sendText(chatid, "some other error occured")
            else:
                t.sendText(chatid, "not enough money bij")

        else: 
            price = df['close'][i]
            t.sendText(chatid, f"Trade has NOT been taken\nat {price}")
            position = 0
    elif (df['10EMA'][i] <= df['50EMA'][i] and position == 1):
        t.sendText(chatid, f"time to close LONG position\n\n/close\n\n/dont_close")
        reply = t.TelebotPoll(30)
        if (reply == '/close'):
            price = df['close'][i]
            t.sendText(chatid, f"Trade has been closed\nat {price}")
            position = 0
            ftx.place_order(market= coin, side= 'sell', price= str(price), type= 'limit', size= 0.001)
            print(order["status"])
        else: 
            price = df['close'][i]
            t.sendText(chatid, f"Trade has NOT been closed\nat {price}")
            position = 1
    elif (df['10EMA'][i] >= df['50EMA'][i] and position == 2):
        t.sendText(chatid, "time to close SHORT position\n\n/close\n\n/dont_close")
        reply = t.TelebotPoll(30)
        if (reply == '/close'):
            price = df['close'][i]
            t.sendText(chatid, f"Trade has been closed\nat {price}")
            position = 0
            order = ftx.place_order(market= coin, side= 'buy', price= str(price), type= 'limit', size= 0.001)
            print(order["status"])
        else: 
            price = df['close'][i]
            t.sendText(chatid, f"Trade has NOT been closed\nat {price}")
            position = 2
    response = t.TelebotPoll(60)
    if (response == "/mybalance"):
        t.sendText(chatid, str(ftx.get_balances()))
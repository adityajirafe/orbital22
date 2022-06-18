import pandas as pd
from firestore_config import *
from datetime import datetime

from trading_functions import *

def get_time():
    time = datetime.now()
    format_data = "%Y-%m-%d, %H:%M:%S"
    return time.strftime(format_data)

def handle_start(job_item, bot):
    bot.sendText(
        "Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your email address",
        job_item.chat_id)
    return 

def handle_username(job_item, bot):
    bot.sendText(
        "Please input your password",
        job_item.chat_id
    )
    return job_item.message

def handle_password(job_item, bot):
    bot.sendText(
        "Thank you",
        job_item.chat_id
    )
    return job_item.message

def handle_logout(job_item, bot):
    chat_id = job_item.chat_id
    del bot.auth_users[chat_id]
    bot.sendText(
        "You have successfully logged out.",
        chat_id
    )
    bot.sendText(
        "Press /start to restart CoinValet",
        chat_id
    )
    return

def handle_sleep(job_item, bot):
    chat_id = job_item.chat_id
    bot.sleep.append(chat_id)
    bot.sendText(
        "Trade suggestions silenced. Press /listen to resume.",
        chat_id
    )
    return

def handle_listen(job_item, bot):
    chat_id = job_item.chat_id
    bot.sleep.remove(chat_id)
    bot.sendText(
        "Listening...",
        chat_id
    )

# checks if there is enough money in the account given the amount required to make a trade
def checkTrade(margin: float, ftx) -> bool:
    s = ftx.get_balances()
    if (s == []):
        return False
    balances = pd.data(s)
    lst = balances.coin.tolist()
    if ("USD" in lst):
        index = lst.index("USD")
        return balances.free[index] > margin
    return False

def handle_long_trade(job_item, bot, margin):
    chat_id = job_item.chat_id
    # retrieves the correct ftx object from the dictionary corresponding to the chat id
    ftx = bot.auth_users[chat_id]
    # stored the specific coin in the job item
    coin = job_item.coin

    email = bot.chatids[chat_id]
    positions = get_positions(email, coin)
    # print(f"positions are {positions}")
    
    # handle_close_trade(positions, 'long', email, bot, chat_id, SIZE) # use for debugging since checkTrade always returns false

    SIZE = 0.001
    # update_position(email, coin, SIZE, 'short', get_time()) # use for debugging since checkTrade always returns false

    # if (checkTrade(margin, ftx)): # use for debugging since checkTrade always returns false
    if True:
        try:
            if (coin not in bot.prices):
                price_update_single(bot, coin, ftx)
            price = bot.prices[coin]

            if len(positions) != 0:
                if handle_close_trade(positions, 'long', email, bot, chat_id, SIZE, price):
                    return    
            # ftx.place_order(market= coin, side= 'buy', price= str(bot.prices[coin]), type= 'limit', size= SIZE)
            bot.sendText(f"Long trade has been taken\n{coin} at ${price}", chat_id)
            # update position here
            time = get_time()
            update_position(email, coin, SIZE, 'long', time)
            
            #update transaction history
            update_trades(
                email, 
                coin, 
                'long', 
                price, 
                time, 
                SIZE, 
                price * SIZE, 
                "OPEN"
            )

        except:
            bot.sendText( "some other error occured", chat_id)
    else:
        bot.sendText("not enough money to make the trade", chat_id)
    print(job_item.message)
    return 

def handle_short_trade(job_item, bot, margin):
    chat_id = job_item.chat_id
    # retrieves the correct ftx object from the dictionary corresponding to the chat id
    ftx = bot.auth_users[chat_id]
    # stored the specific coin in the job item
    coin = job_item.coin
    
    email = bot.chatids[chat_id]
    positions = get_positions(email, coin)
    # print(f"positions are {positions}")
    
    # handle_close_trade(positions, 'short', email, bot, chat_id, SIZE) # use for debugging since checkTrade always returns false
    
    SIZE = 0.001
    # update_position(email, coin, SIZE, 'short', get_time()) # use for debugging since checkTrade always returns false

    # if (checkTrade(margin, ftx)): # use for debugging since checkTrade always returns false
    if True:
        try:
            if (coin not in bot.prices):
                price_update_single(bot, coin, ftx)
            price = bot.prices[coin]

            if len(positions) != 0:
                if handle_close_trade(positions, 'short', email, bot, chat_id, SIZE, price): 
                    return

            # ftx.place_order(market= coin, side= 'sell', price= str(bot.prices[coin]), type= 'limit', size= SIZE)
            bot.sendText(f"Short trade has been taken\n{coin} at ${bot.prices[coin]}", chat_id)
            # update position here
            time = get_time()
            update_position(email, coin, SIZE, 'short', time)

            #update transaction history
            update_trades(
                email, 
                coin, 
                'short', 
                price, 
                time, 
                SIZE, 
                price * SIZE, 
                "OPEN"
            )
                
        except:
            bot.sendText( "some other error occured", chat_id)
    else:
        bot.sendText(f"not enough money to make the trade for {coin}", chat_id)
        print("no money")

    # ftx.place_order(market= coin, side= 'sell', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
    # bot.sendText(f"Short trade has been taken\n{coin} at {bot.prices[coin]}", chat_id)
    print(job_item.message)
    return 


def handle_close_trade(positions, favoured_trade, email, bot, chat_id, units, price):
    # print(positions)
    num_trades_closed = 0
    for doc_id, position in positions:
        # eg of position: {'name': 'long', 'units': '0.0083', 'price': '$41,803.43', 'coin': 'BTC', 'value': '$346.97', 'time': '2022-03-01, 16:52:45'}

        if (position['name'] == favoured_trade):
            continue
        else:
            print(f"{position['coin']} {position['name']} opened on {position['time']} has been closed")
            """Sample Output:
            BTC long closed
            BTC short closed
            BTC short closed"""

            # close trade on ftx

            # remove position from firestore
            delete_position(email, doc_id) # COMMENT OUT FOR DEBUGGING -> prevent unnecessary deletion of firebase data
            
            # update transaction history
            update_trades(
                email, 
                position['coin'], 
                position['name'], 
                price, 
                get_time(), 
                units, 
                price * units, 
                "CLOSED"
            )

            # the send message code below to be moved to the close_trade function after successfully closing trade on ftx
            bot.sendText(
                f"{position['coin']} {position['name']} opened on {position['time']} has been closed", 
                chat_id
            )
            num_trades_closed += 1
    
    if num_trades_closed > 0:
        bot.sendText(
                f"To open {favoured_trade} position, click on \n/{favoured_trade}_trade_{position['coin']} again",
                chat_id
            )
        return True
    else:
        return False
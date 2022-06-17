import pandas as pd
from firestore_config import *

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
    print(f"positions are {positions}")
    
    handle_close_trade(positions, 'short', email, bot, chat_id) # use for debugging since checkTrade always returns false

    if (checkTrade(margin, ftx)):
        try:
            if len(positions) != 0:
                handle_close_trade(positions, 'long', email, bot, chat_id)
            else:
                ftx.place_order(market= coin, side= 'buy', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
                bot.sendText(f"Long trade has been taken\n{coin} at {bot.prices[coin]}", chat_id)
                # update position here
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
    print(f"positions are {positions}")
    
    handle_close_trade(positions, 'short', email, bot, chat_id) # use for debugging since checkTrade always returns false

    if (checkTrade(margin, ftx)):
        try:
            if len(positions) != 0:
                handle_close_trade(positions, 'short', email, bot, chat_id)
            else:                
                ftx.place_order(market= coin, side= 'sell', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
                bot.sendText(f"Short trade has been taken\n{coin} at {bot.prices[coin]}", chat_id)
                # update position here
        except:
            bot.sendText( "some other error occured", chat_id)
    else:
        bot.sendText(f"not enough money to make the trade for {coin}", chat_id)
        print("no money")

    # ftx.place_order(market= coin, side= 'sell', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
    # bot.sendText(f"Short trade has been taken\n{coin} at {bot.prices[coin]}", chat_id)
    print(job_item.message)
    return 

def handle_no_trade(job_item, bot):
    bot.sendText(
        "Trade NOT executed",
        job_item.chat_id
    )
    print(job_item.message)
    return 

def handle_close_trade(positions, favoured_trade, email, bot, chat_id):
    # print(positions)
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
            #delete_position(email, doc_id) # COMMENT OUT FOR DEBUGGING -> prevent unnecessary deletion of firebase data
            
            # the send message code below to be moved to the close_trade function after successfully closing trade on ftx
            bot.sendText(
                f"{position['coin']} {position['name']} opened on {position['time']} has been closed", 
                chat_id
            )
            pass
    return 
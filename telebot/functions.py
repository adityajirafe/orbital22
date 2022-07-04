import pandas as pd
from datetime import datetime, timedelta
from firestore_config import *

from trading_functions import *
from portfolio_metrics import *


"""Gets current time"""
def get_time():
    time = datetime.now() + timedelta(minutes= 480)
    format_data = "%Y-%m-%d, %H:%M:%S"
    return time.strftime(format_data)


"""Handles /start input"""
def handle_start(job_item, bot):
    bot.sendText(
        "Welcome to CoinValet (by Aditya and Cheng Yang)\n\nPlease input your email address!\nYou have 30 seconds to do so.",
        job_item.chat_id)
    return 


"""Handles users inputting their email address"""
def handle_username(job_item, bot):
    bot.sendText(
        "Please input your password!\nYou have 30 seconds to do so.",
        job_item.chat_id
    )
    return job_item.message.lower()


"""Handles users inputting their password"""
def handle_password(job_item, bot):
    bot.sendText(
        "Thank you",
        job_item.chat_id
    )
    return job_item.message


"""Handles users logging out"""
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


"""Handles users silencing trade suggestions"""
def handle_sleep(job_item, bot):
    chat_id = job_item.chat_id
    bot.sleep.append(chat_id)
    bot.sendText(
        "Trade suggestions silenced. Press /listen to resume.",
        chat_id
    )
    return


"""Handles users un-silencing trade suggestions"""
def handle_listen(job_item, bot):
    chat_id = job_item.chat_id
    bot.sleep.remove(chat_id)
    bot.sendText(
        "Listening...",
        chat_id
    )

"""Handles users checking their balance in their FTX account"""
def handle_balance(job_item, bot):
    chat_id = job_item.chat_id
    # ftx = bot.auth_users[chat_id]
    ftx = bot.master_ftxobj
    balance = ftx.get_balances()
    mybalance = ''
    for coin in balance:
        c = coin['coin']
        total = coin['total']
        value = coin['usdValue']
        if total != 0:
            sentence = f'{c}\namount: {total}\nvalue: {value} USD\n\n'
            mybalance = mybalance + sentence
    
    print(mybalance)
    bot.sendText(mybalance, chat_id)


"""Handles no trade events"""
def handle_no_trade(job_item, bot):
    print('inside handle no trade')
    chat_id = job_item.chat_id
    coin = job_item.coin
    print('about to send text')
    bot.sendText(
        f"{coin} trade NOT taken",
        chat_id
    )
    return

"""checks for enough money in account given the amount required to trade"""
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


"""Handles users executing a long trade"""
def handle_long_trade(job_item, bot, margin):
    chat_id = job_item.chat_id
    # retrieves the correct ftx object from the dictionary corresponding to the chat id
    ftx = bot.auth_users[chat_id]
    # stored the specific coin in the job item
    coin = job_item.coin

    email = bot.chatids[chat_id]
    positions = get_positions(email, coin)
    print(f"positions: {positions}")

    SIZE = bot.coins_and_qty[coin + "-PERP"]
    # if (checkTrade(margin, ftx)): # use for debugging since checkTrade always returns false
    if True:
        try:
            """Retrieves coin price"""
            if (coin not in bot.prices):
                price_update_single(bot, coin, bot.master_ftxobj)
            price = bot.prices[coin]

            """Checks current positions and closes unfavourable trades"""
            if len(positions) != 0:
                if handle_close_trade(positions, 'long', email, bot, chat_id):
                    print("close trade")
                    return    
            # ftx.place_order(market= coin, side= 'buy', price= str(price), type= 'limit', size= SIZE)
            bot.sendText(
                f"Long trade has been taken\n{coin} at ${price} and {SIZE} units", 
                chat_id
            )
            print("after text")
            time = get_time()

            """Updates position on firebase"""
            update_position(email, coin, SIZE, 'long', time, price)
            
            """Updates transaction history on firebase"""
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
            bot.sendText(
                "some other error occured", 
                chat_id
            )
    else:
        bot.sendText(
            "not enough money to make the trade", 
            chat_id
        )
    print(job_item.message) #Debugging statement
    return 


"""Handles users executing short trades"""
def handle_short_trade(job_item, bot, margin):
    chat_id = job_item.chat_id
    ftx = bot.auth_users[chat_id]
    coin = job_item.coin
    
    email = bot.chatids[chat_id]
    positions = get_positions(email, coin)

    print(bot.coins_and_qty[coin + "-PERP"])
    SIZE = bot.coins_and_qty[coin + "-PERP"]

    # if (checkTrade(margin, ftx)): # use for debugging since checkTrade always returns false
    if True:
        try:
            """Retrieves coin price"""
            if (coin not in bot.prices):
                price_update_single(bot, coin, bot.master_ftxobj)
            price = bot.prices[coin]

            """Checks current positions and closes unfavourable trades"""            
            if len(positions) != 0:
                if handle_close_trade(positions, 'short', email, bot, chat_id): 
                    return

            # ftx.place_order(market= coin, side= 'sell', price= str(price), type= 'limit', size= SIZE)
            bot.sendText(
                f"Short trade has been taken\n{coin} at ${price} and {SIZE} units", 
                chat_id
            )
            time = get_time()
            
            """Update position on firebase"""
            update_position(email, coin, SIZE, 'short', time, price)

            """Update transaction history on firebase"""
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
            bot.sendText(
                "some other error occured", 
                chat_id
            )
    else:
        bot.sendText(
            f"not enough money to make the trade for {coin}", 
            chat_id
        )
    print(job_item.message) #Debugging Statement
    return 


"""Handles users closing trade positions"""
def handle_close_trade(positions, favoured_trade, email, bot, chat_id):
    num_trades_closed = 0
    order_type = ''
    if favoured_trade == 'long':
        order_type = 'buy'
    elif favoured_trade == 'short':
        order_type = 'sell'
    for doc_id, position in positions:
        # eg of position: {'name': 'long', 'qty': '0.0083', 'price': '$41,803.43', 'coin': 'BTC', 'value': '$346.97', 'time': '2022-03-01, 16:52:45'}
        qty = position['qty']
        coin = position['coin']
        price = bot.prices[coin]
        
        if (position['name'] == favoured_trade):
            continue
        else:
            print(f"{coin} {position['name']} opened on {position['time']} has been closed")
            """Sample Output:
            BTC long closed
            BTC short closed
            BTC short closed"""

            """close trade on ftx"""
            # ftx.place_order(market= coin, side= order_type, price= str(price), type= 'limit', size= qty)

            """Update portfolio metrics"""
            sell_value = price * qty
            upload_realised_profit(email, doc_id, sell_value)
            update_metrics(bot, bot.coins, bot.master_ftxobj, email)
            """Removes position on firebase"""
            delete_position(email, doc_id) # COMMENT OUT FOR DEBUGGING -> prevent unnecessary deletion of firebase data
            
            """Updates user trade history on firebase"""
            update_trades(
                email, 
                coin, 
                position['name'], 
                price, 
                get_time(), 
                qty, 
                price * qty, 
                "CLOSED"
            )
            
            print(f"updated metrics after trade closed by {email}")
            bot.sendText(
                f"{coin} {position['name']} opened on {position['time']} has been closed", 
                chat_id
            )
            num_trades_closed += 1
    
    """Prompt users to re-input prompt after closing unfavourable trades"""
    if num_trades_closed > 0:
        bot.sendText(
                f"To open {favoured_trade} position, click on \n\n/{favoured_trade}_trade_{coin} again",
                chat_id
            )
        return True
    else:
        return False
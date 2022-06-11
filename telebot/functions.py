import pandas as pd

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

def handle_long_trade(job_item, bot):
    chat_id = job_item.chat_id
    # retrieves the correct ftx object from the dictionary corresponding to the chat id
    ftx = bot.auth_users[chat_id]
    # stored the specific coin in the job item
    coin = job_item.coin

    if (checkTrade(1, ftx)):
        try:
            ftx.place_order(market= coin, side= 'buy', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
            bot.sendText(f"Long trade has been taken\nat {bot.prices[coin]}", chat_id)
            # update position here
        except:
            bot.sendText( "some other error occured", chat_id)
    else:
        bot.sendText("not enough money to make the trade", chat_id)
    print(job_item.message)
    return 

def handle_short_trade(job_item, bot):
    chat_id = job_item.chat_id
    # retrieves the correct ftx object from the dictionary corresponding to the chat id
    ftx = bot.auth_users[chat_id]
    # stored the specific coin in the job item
    coin = job_item.coin

    if (checkTrade(1, ftx)):
        try:            
            ftx.place_order(market= coin, side= 'sell', price= str(bot.prices[coin]), type= 'limit', size= 0.001)
            bot.sendText(f"Short trade has been taken\nat {bot.prices[coin]}", chat_id)
            # update position here
        except:
            bot.sendText( "some other error occured", chat_id)
    else:
        bot.sendText("not enough money to make the trade", chat_id)
        print("no money")

    print(job_item.message)
    return 

def handle_no_trade(job_item, bot):
    bot.sendText(
        "Trade NOT executed",
        job_item.chat_id
    )
    print(job_item.message)
    return 
import mplfinance as fplt
import pandas as pd
from FTXAPI import FtxClient
import talib as ta
from firestore_config import *

def shortform(coin: str):
    # count = 0
    # for letter in coin:
    #     if letter == "-":
    #         break
    #     else:
    #         count+= 1
    # return coin[0:count]

    return coin.split('-')[0]


def price_update(coins, ftx):
    price_list = []
    for coin in coins:
        df = getData(coin, '1h', ftx)
        last_entry_index = len(df) - 1
        price = df['close'][last_entry_index]
        shortened_coin = shortform(coin)
        price_list.append((shortened_coin, price))
    print(price_list)
    return update_prices(price_list)


def trading_algo(bot, coin, interval, ftx):
    # trivial check to skip if no users logged in
    if bot.auth_users == {}:
        return
    # run for one coin first -> BTC
    shortened_coin = shortform(coin)
    # gets the first key of the dictionary which is a chat id
    # temp_chat_id = list(bot.auth_users.keys())[0]
    # gets the ftx object tagged to that chat id
    # ftx = bot.auth_users[temp_chat_id]

    active_users = list(bot.auth_users.keys())
    for user in bot.sleep:
        if user in active_users:
            active_users.remove(user)
    
    if active_users == []:
        return
    
    suggested_trade = detect_trade(bot, coin, interval, ftx)
    price = suggested_trade['price']
    
    # store the coin and its price in the dictionary to be accessed later on
    bot.update_coin_prices(coin, price)
    
    for chat_id in active_users:
        bot.sendImage(f"{coin}.png", chat_id)
        if (suggested_trade['type'] == 'LONG'):
            bot.sendText(
                f"{shortened_coin} price is currently {price} USD\nFavoured trade: {suggested_trade['type']} at {price} USD\n\n/long_trade_{shortened_coin}\n\n/no_trade",
                chat_id
            )
        elif (suggested_trade['type'] == 'SHORT'):
            bot.sendText(
                f"{shortened_coin} price is currently {price} USD\nFavoured trade: {suggested_trade['type']} at {price} USD\n\n/short_trade_{shortened_coin}\n\n/no_trade",
                chat_id
            )
        elif (suggested_trade['type'] == 'NO_TRADE'):
            bot.sendText(f"{shortened_coin} price is currently {price} USD\nno trade detected for {shortened_coin}")


"""To plot the graph of specified coin and save it"""
def plot_and_save(coin: str, interval: str, ftx: FtxClient):
    df = getData(coin, interval, ftx)
    df = df.tail(150)
    #plotting the graph and saving it
    ap2 = [fplt.make_addplot(df['50EMA'], color='#180dad', panel= 1), 
            fplt.make_addplot(df['10EMA'], color='#ffff40', panel= 1),
            fplt.make_addplot(df['RSI'], color='#6a0dad', panel= 2)]

    fplt.plot(
            df,
            type='candle',
            style= 'charles',
            title= coin + ' chart',
            ylabel='Price ($)',
            main_panel= 1,
            addplot= ap2,
            savefig= f"{coin}.png" #change to coin name
    )


"""To pull data of specified coin from FTX API"""
def getData(coin: str, time: str, ftx: FtxClient):

    # Pulling dataframe from FTX API
    df = ftx.get_market_data(coin, time)
    df = ftx.parse_ftx_response(df.json()) #what does this do 
    df.index = pd.to_datetime(df.index, infer_datetime_format = True)

    # Adding the RSI column
    df['RSI'] = ta.RSI(df['close'], timeperiod = 9)

    # Adding the 50 day EMA
    df['50EMA'] = ta.EMA(df['close'], timeperiod = 50)

    # Adding the 10 day EMA
    df['10EMA'] = ta.EMA(df['close'], timeperiod = 10)
    return df


"""To detect potential trades"""
def detect_trade(bot, coin, interval, ftx) -> dict:
    print(f'Detecting trades for {coin}')

    # try:
    df = getData(coin, interval, ftx)

    plot_and_save(coin, interval, ftx)

    last_entry_index = len(df) - 1
    price = df['close'][last_entry_index]

    print(f"Price of {coin} is {price}")

    EMA_10 = df['10EMA'][last_entry_index]
    EMA_50 = df['50EMA'][last_entry_index]

    if EMA_10 > EMA_50:
        print('detected favour long')
        return {'type': "LONG", 'price': price}
    elif EMA_10 < EMA_50:
        print('detected favour short')
        return {'type': "SHORT", 'price': price}
    else: 
        print('detected no trade')
        return{'type': "NO_TRADE", 'price': price}

    # if (df['10EMA'][last_entry_index] > df['50EMA'][last_entry_index] and position == 0):
    #     t.sendText(f"Trading on the {interval} interval chart\nTime to open LONG position\n\n/trade\n\n/no_trade")
    #     print(f'finish detect trade for {chatid}')
    #     return {'type': 'OPENLONG', 'price': price}
    # elif (df['10EMA'][last_entry_index] < df['50EMA'][last_entry_index] and position == 0):
    #     t.sendText(f"Trading on the {interval} interval chart\nTime to open SHORT position\n\n/trade\n\n/no_trade")            
    #     print(f'finish detect trade for {chatid}')
    #     return {'type': 'OPENSHORT', 'price': price}
    # elif (df['10EMA'][last_entry_index] < df['50EMA'][last_entry_index] and position == 1):
    #     t.sendText(f"Trading on the {interval} interval chart\nTime to close LONG position\n\n/close\n\n/dont_close")
    #     print(f'finish detect trade for {chatid}')
    #     return {'type': 'CLOSELONG', 'price': price}
    # elif (df['10EMA'][last_entry_index] > df['50EMA'][last_entry_index] and position == 2):
    #     t.sendText(f"Trading on the {interval} interval chart\nTime to close SHORT position\n\n/close\n\n/dont_close")
    #     print(f'finish detect trade for {chatid}')
    #     return {'type': 'CLOSESHORT', 'price': price}
    # else:
    #     print(f'finish detect trade for {chatid}')
    #     return {'type': 'notradedetected', 'price': price}
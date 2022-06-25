import mplfinance as fplt
import pandas as pd
from FTXAPI import FtxClient
import talib as ta
from firestore_config import *

"""Changes coin naming convention"""
def shortform(coin: str):
    return coin.split('-')[0]


"""Pulls data from FTX api on coin prices"""
def get_prices(bot, coins, ftx):
    price_list = []
    for coin in coins:
        df = getData(coin, '1h', ftx)
        last_entry_index = len(df) - 1
        price = df['close'][last_entry_index]
        shortened_coin = shortform(coin)
        price_list.append((shortened_coin, price))
        # store coin price
        bot.update_coin_prices(shortened_coin, price)

    return price_list


"""Updates the coin prices stored inside the bot"""
def price_update(bot, coins, ftx):
    price_list = get_prices(bot, coins, ftx)
    return update_prices(price_list)


"""Pulls data from FTX api on particular coin price"""
def price_update_single(bot, coin, ftx):
    price_list = []
    df = getData(f"{coin}-PERP", '1h', ftx)
    last_entry_index = len(df) - 1
    price = df['close'][last_entry_index]
    price_list.append((coin, price))
    # store coin price
    bot.update_coin_prices(coin, price)
    return update_prices(price_list)


"""Detects and suggests trade positions"""
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
    
    suggested_trade = detect_trade(coin, interval, ftx)
    price = suggested_trade['price']
    
    # store the coin and its price in the dictionary to be accessed later on
    bot.update_coin_prices(shortened_coin, price)
    
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


"""Plots the graph of specified coin and saves it"""
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


"""Pulls data of specified coin from FTX API"""
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


"""Detects potential trades"""
def detect_trade(coin, interval, ftx) -> dict:
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
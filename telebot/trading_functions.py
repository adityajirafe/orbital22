import mplfinance as fplt
import pandas as pd
from FTXAPI import FtxClient
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
        email = bot.chatids[chat_id]
        positions = get_positions(email, shortened_coin)
        print(f"positions: {positions}")
        
        if len(positions) == 0:
            bot.sendImage(f"{coin}.png", chat_id)
            if (suggested_trade['type'] == 'LONG'):
                bot.sendText(
                    f"{shortened_coin} price is currently {price} USD\nFavoured trade: {suggested_trade['type']} at {price} USD\n\n/long_trade_{shortened_coin}\n\n/no_trade_{shortened_coin}",
                    chat_id
                )
            elif (suggested_trade['type'] == 'SHORT'):
                bot.sendText(
                    f"{shortened_coin} price is currently {price} USD\nFavoured trade: {suggested_trade['type']} at {price} USD\n\n/short_trade_{shortened_coin}\n\n/no_trade_{shortened_coin}",
                    chat_id
                )
            elif (suggested_trade['type'] == 'NO_TRADE'):
                bot.sendText(f"{shortened_coin} price is currently {price} USD\nno trade detected for {shortened_coin}")
        else:
            for trade in positions:
                if trade[1]['coin'] == shortened_coin:
                    if suggested_trade['type'] != trade[1]['name'].upper():
                        bot.sendText(
                            f"{shortened_coin} price is currently {price} USD\nClose {trade[1]['name'].upper()} trade at {price} USD\n\n/close_{trade[1]['name']}_{shortened_coin}\n\n/no_trade_{shortened_coin}",
                            chat_id
                        )
"""Plots the graph of specified coin and saves it"""
def plot_and_save(coin: str, interval: str, ftx: FtxClient):
    df = getData(coin, interval, ftx)
    df = df.tail(150)
    #plotting the graph and saving it
    ap2 = [fplt.make_addplot(df['10EMA'], color='#180dad', panel= 1), 
            fplt.make_addplot(df['25EMA'], color='#FFA500', panel= 1),
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
    df['close_delta'] = df['close'].diff()
    df['up'] = df['close_delta'].clip(lower=0)
    df['down'] = -1 * df['close_delta'].clip(upper=0)

    df['ema_up'] = df['up'].ewm(com = 13, adjust = False).mean()
    df['ema_down'] = df['down'].ewm(com = 13, adjust = False).mean()
    df['RSI']= 100 - (100/(1 + df['ema_up']/df['ema_down']))

    # Adding the 25 day EMA
    df['25EMA'] = df['close'].ewm(span=25, adjust=False).mean()
    
    # Adding the 10 day EMA
    df['10EMA'] = df['close'].ewm(span=10, adjust=False).mean()
    return df


"""Detects potential trades"""
def detect_trade(coin, interval, ftx) -> dict:
    print(f'Detecting trades for {coin}')

    # try:
    df = getData(coin, interval, ftx)

    plot_and_save(coin, interval, ftx)

    last_entry_index = len(df) - 1
    price = df['close'][last_entry_index]
    
    EMA_10 = df['10EMA'][last_entry_index]
    EMA_25 = df['25EMA'][last_entry_index]

    if EMA_10 > EMA_25:
        return {'type': "LONG", 'price': price}
    elif EMA_10 < EMA_25:
        return {'type': "SHORT", 'price': price}
    else: 
        return{'type': "NO_TRADE", 'price': price}
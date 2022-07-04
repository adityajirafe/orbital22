from firestore_config import db
from trading_functions import get_prices, shortform


"""Retrieve all active positions held by user"""
def get_all_positions(email):
    try:
        reference = db.collection(u'UserPortfolio', f"{email}", u'positions')
        docs = reference.stream()

        list_of_positions = []
        for doc in docs:
            list_of_positions.append( (doc.to_dict()) )
        return list_of_positions
    except:
        print('ERROR in getting positions')
        return []


"""Consolidates positions of duplicate coins"""
def consolidate_positions(email):
    list_of_positions = get_all_positions(email)
    consolidated_positions = {}
    for position in list_of_positions:
        coin = position['coin']
        name = position['name']
        if coin not in consolidated_positions:
            consolidated_positions[coin] = {'qty': 0, 'value': 0, 'name': name}
        consolidated_positions[coin]['qty'] = consolidated_positions[coin]['qty'] + position['qty']
        consolidated_positions[coin]['value'] = consolidated_positions[coin]['value'] + (position['qty'] * position['price'])

    return consolidated_positions


"""Calculates the profits made from each position"""
def get_profits(bot, coins, ftx, email):
    positions = consolidate_positions(email)
    profits = {}
    print("start pulling prices")
    prices = get_prices(bot, coins, ftx)
    price_directory = {}
    """Process prices"""
    for i in prices:
        coin = i[0]
        price = i[1]
        price_directory.update({coin: price})
    for c in coins:
        coin = shortform(c)
        if coin not in positions:
            continue
        value = positions[coin]['value']
        current_value = price_directory[coin] * positions[coin]['qty']
        if positions[coin]['name'] == 'long':
            profit = current_value - value
        elif positions[coin]['name'] == 'short':
            profit = value - current_value 
        profits.update({coin: profit})
    return profits 


"""Uploads specified portfolio metric on firestore, without overriding previous data"""
def upload_metric(email, docRef, data):
    reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
    reference.document(docRef).set(data, merge = True)


"""Uploads specified portfolio metric on firestore, with overriding previous data"""
def override_metric(email, docRef, data):
    reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
    reference.document(docRef).set(data)


"""Retrieves best position held by user"""
def get_best_position(profits, email):
    profits = list(profits.items())
    positions = consolidate_positions(email)
    best_coin = profits[0]
    for pair in profits:
        coin = pair[0]
        profit = pair[1]
        current_returns = (float(profit) / float(positions[coin]['value']) * 100)
        if current_returns > (best_coin[1] / float(positions[best_coin[0]]['value']) * 100):
            best_coin = pair

    position = []
    position.append(best_coin[0])
    position.append((float(best_coin[1])/ float(positions[best_coin[0]]['value'])) * 100)
    return position

"""Retrieves worst position held by user"""
def get_worst_position(profits, email):
    profits = list(profits.items())
    positions = consolidate_positions(email)
    worst_coin = profits[0]
    for pair in profits:
        coin = pair[0]
        profit = pair[1]
        current_returns = (float(profit) / float(positions[coin]['value']) * 100)
        if current_returns < (worst_coin[1] / float(positions[worst_coin[0]]['value']) * 100):
            worst_coin = pair

    position = []
    position.append(worst_coin[0])
    position.append((float(worst_coin[1])/ float(positions[worst_coin[0]]['value'])) * 100)
    return position


"""Handles and uploads realised profits on firestore"""
def upload_realised_profit(email, doc_reference, sell_value, opened_trade):
    reference = db.collection(u'UserPortfolio', f"{email}", u'positions')
    doc_ref = reference.document(f"{doc_reference}").get()
    doc_data = doc_ref.to_dict()
    initial_value = doc_data['price'] * doc_data['qty']
    
    if (opened_trade == 'long'):
        realised_profit = sell_value - initial_value
    else:
        realised_profit =  initial_value - sell_value
    time = doc_data['time']
    data = {time: realised_profit}
    upload_metric(email, 'realised_transactions', data)
    set_realised_profits(email)
    return realised_profit


"""Calculates realised profits and uploads tabulated amount"""
def set_realised_profits(email):
    reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
    realised_transactions = reference.document('realised_transactions').get().to_dict()
    realised_profits = 0
    for k,v in realised_transactions.items():
        realised_profits += v
    data = {'value': realised_profits}
    override_metric(email, 'realised_profits', data)


"""Calculates all-time PnL (%) and uploads it"""
def upload_all_time_profits_percentage(email, all_time_profits):
    positions = consolidate_positions(email)
    total_value = 0
    for coin, values in positions.items():
        total_value += values['value']
    percentage = all_time_profits / total_value * 100
    data = {'value': percentage}
    override_metric(email, 'all-time_PnL_percentage', data)


"""Calculates 24-h PnL (%) and uploads it"""
def upload_daily_profits_percentage(email, daily_profits):
    positions = consolidate_positions(email)
    total_value = 0
    for coin, values in positions.items():
        total_value += values['value']
    percentage = daily_profits / total_value * 100
    data = {'value': percentage}
    override_metric(email, 'daily_PnL_percentage', data)


"""Calculates all-time profits"""
def set_all_time_profits(profits, email):
    unrealised_profits = 0
    for coin, profit in profits.items():
        unrealised_profits += profit
    realised_profit_reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
    realised_profits_doc = realised_profit_reference.document('realised_profits').get()
    if realised_profits_doc.exists:
        realised_profits = realised_profits_doc.to_dict()['value']
    else: 
        realised_profits = 0
    all_time_profits = realised_profits + unrealised_profits
    data = {'value': all_time_profits}
    override_metric(email, 'all-time_PnL', data)
    upload_all_time_profits_percentage(email, all_time_profits)

def set_24h_profits(profits, email):
    unrealised_profits = 0
    for coin, profit in profits.items():
        unrealised_profits += profit
    ytd_profit_reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
    ytd_profit_doc = ytd_profit_reference.document('ytd_PnL').get()
    if ytd_profit_doc.exists:
        ytd_profit = ytd_profit_doc.to_dict()['value']
        daily_profit = unrealised_profits - ytd_profit
        """Upload numeric 24h profit"""
        daily_profit_data = {'value': daily_profit}
        override_metric(email, 'daily_PnL', daily_profit_data)
        print('dailyPnL done')

        """Upload percentage 24h profit"""
        upload_daily_profits_percentage(email, daily_profit)
        print('dailyPnLPercent done')

        """Overwrite ytd profits"""
        ytd_profit_data = {'value': unrealised_profits}
        override_metric(email, 'ytd_PnL', ytd_profit_data)
        print('ytdPnL done')

    else:
        print("not enough data")
        """Upload numeric 24h profit"""
        daily_profit_data = {'value': 'NA'}
        override_metric(email, 'daily_PnL', daily_profit_data)
        print('dailyPnL done')

        """Upload percentage 24h profit"""
        daily_percent_data = {'value': 'NA'}
        override_metric(email, 'daily_PnL_percentage', daily_percent_data)
        print('dailyPnLPercent done')

        """Overwrite ytd profits"""
        ytd_profit_data = {'value': unrealised_profits}
        override_metric(email, 'ytd_PnL', ytd_profit_data)
        print('ytdPnL done')
    
    return 

"""Dispatches updates for the various metrics on firestore"""
def update_metrics(bot, coins, ftx, email):
    
    profits = get_profits(bot, coins, ftx, email)
    
    """Finds and uploads best position held by user onto firestore"""
    best_position = get_best_position(profits, email)
    best_position_data = {'value': best_position[1], 'coin': best_position[0]}
    override_metric(email, 'best_position', best_position_data)
    print('best position done')
    
    """Finds and uploads worst position held by user onto firestore"""
    worst_position = get_worst_position(profits, email)
    worst_position_data = {'value': worst_position[1], 'coin': worst_position[0]}
    override_metric(email, 'worst_position', worst_position_data)
    print('worst position done')

    """Finds and uploads all time profits onto firestore"""
    set_all_time_profits(profits, email)
    print('all time done')

    """Finds and uploads 24h profits onto firestore"""
    set_24h_profits(profits, email)
    print('daily done')

    return 

# doc_ref = db.document(u"UserPortfolio", 'adi', u'metrics', u'realised_profits')
# doc = doc_ref.get()
# print(doc.exists)

# email = 'adi@gmail.com'
# ytd_profit_reference = db.collection(u"UserPortfolio", f"{email}", u'metrics')
# ytd_profit_doc = ytd_profit_reference.document('ytd_position').get()
# print(ytd_profit_doc.exists)
import firebase_admin

from firebase_admin import credentials, firestore

cred = credentials.Certificate('telebot/ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# def get_trial():
#     museums = db.collection_group(u'landmarks')\
#         .where(u'type', u'==', u'museum')
#     docs = museums.stream()
#     lst = []
#     for doc in docs:
#         lst.append(doc.to_dict())

#     print(lst)

"""Used to get list of positions held by user for a specific coin"""
def get_positions(email, coin): 
    try:
        reference = db.collection(u'UserPortfolio', f"{email}", u'positions')
        query_ref = reference.where(u'coin', u'==', f"{coin}")
        docs = query_ref.stream()

        list_of_positions = []
        for doc in docs:
            list_of_positions.append( (doc.id, doc.to_dict()) )
        return list_of_positions
    except:
        print('ERROR in getting positions')
        return []


"""Used to update positions held by user after opening position"""
def update_position(email, coin, qty, name, time):
    reference = db.collection(u"UserPortfolio", f"{email}", u'positions')
    reference.add({'coin': coin, 'qty': qty, 'name': name, 'time': time})


"""Used to delete positions held by user after closing position"""
def delete_position(email, doc_reference):
    reference = db.collection(u'UserPortfolio', f"{email}", u'positions')
    doc_ref = reference.document(f"{doc_reference}")
    doc_ref.delete()
    return


"""Used to add coin prices to firebase"""
def update_prices(price_list):
    for coin, price in price_list:
        reference = db.document(u'Prices', f"{coin}")
        reference.update({'price' : price})
        print(f"{coin} updated. price: {price}")


"""Used to update trade history of user on firebase"""
def update_trades(email, coin, name, price, time, units, value, action):
    reference = db.collection(u"UserPortfolio", f"{email}", u'trades')
    reference.add({
        'coin': coin, 
        'name': name, 
        'price': price, 
        'time': time, 
        'units': units, 
        'value': value,
        'action': action
    })


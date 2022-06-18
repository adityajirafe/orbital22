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
    print(f"email is {email}")
    print(f"coin is {coin}")
    try:
        reference = db.collection(u'UserPortfolio', f"{email}", u'trades')
        query_ref = reference.where(u'coin', u'==', f"{coin}")
        docs = query_ref.stream()

        list_of_positions = []
        for doc in docs:
            list_of_positions.append( (doc.id, doc.to_dict()) )
        return list_of_positions
    except:
        print('ERROR in getting positions')
        return []

"""Used to delete positions held by user after closing position"""
def delete_position(email, doc_reference):
    reference = db.collection(u'UserPortfolio', f"{email}", u'trades')
    doc_ref = reference.document(f"{doc_reference}")
    doc_ref.delete()
    return

def update_prices(price_list):
    for coin, price in price_list:
        reference = db.document(u'Prices', f"{coin}")
        reference.update({'price' : price})
        print(f"{coin} updated. price: {price}")

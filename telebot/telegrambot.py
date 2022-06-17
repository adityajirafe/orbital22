import requests
from datetime import timedelta, datetime

class TelegramBot:
    def __init__(self, botToken: str):
        self.botToken = botToken
        # self.initialised = False
        self.chatids = {}
        self.auth_users = {}
        self.prices = {}

    def TelebotPoll(self, waitTime: int):

        site = f'https://api.telegram.org/bot{self.botToken}/getUpdates'
        data = requests.get(site).json()  # reads data from the url getUpdates
        
        ## Store the update id to compare new messages to 
        old_update_id = data['result'][0]['update_id'] #replace with -1
        time = datetime.now()
        waitingTime = time + timedelta(seconds=waitTime)
        result = []

        while True:
            if waitingTime < datetime.now():
                result = []
                break
            data = requests.get(site).json()  # reads data from the url getUpdates
            if (data['result'] != []):
                for entry in data['result']:
                    new_update_id = entry['update_id']
                    if new_update_id <= old_update_id:
                        continue
                    elif new_update_id > old_update_id:
                        chat_id = str(entry['message']['chat']['id'])  # reads chat ID
                        name = str(entry['message']['chat']['first_name'])  # reads username
    
                        text = str(entry['message']['text'])  # reads what they have sent
                        requests.get(f'https://api.telegram.org/bot{self.botToken}/getUpdates?offset=' + str(new_update_id))
                        result.append({'first_name': name, 'chat_id': chat_id, 'message': text})
                        print(result)
                        continue
                
                return result        
        return result
        

    def sendText(self, message, chat_id):
        URL=f"https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(URL)

    def sendImage(self, directory, chat_id):
        try:
            imgpath = {'photo': open(directory, 'rb')}
            requests.post(
                f'https://api.telegram.org/bot{self.botToken}/sendPhoto?chat_id={chat_id}',
                files=imgpath)  # Sending Automated Image
            print("Image Sent")
        except:
            print("Failed to send Image")

    def authenticate_user(self, chat_id, ftxobj):
        self.auth_users[chat_id] = ftxobj
        print(self.auth_users)

    def store_email(self, chat_id, email):
        self.chatids[chat_id] = email
        
    def update_coin_prices(self, coin, price):
        self.prices[coin] = price
        print(self.prices)

    # def initialise_bot(self):
    #     self.initalised = True
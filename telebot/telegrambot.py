from re import L
import requests
from datetime import timedelta, datetime

class TelegramBot:
    def __init__(self, botToken: str, chatid: str, graphDirectory: str):
        self.botToken = botToken
        self.chatid = chatid
        self.graphDirectory = graphDirectory

    def TelebotPoll(self, waitTime):
        site = f'https://api.telegram.org/bot{self.botToken}/getUpdates'
        data = requests.get(site).json()  # reads data from the url getUpdates
        lastMsg = len(data['result']) - 1
        updateIdSave = data['result'][lastMsg]['update_id']
        time = datetime.now()
        waitingTime = time + timedelta(seconds=waitTime)
        text = ''

        while True:
            data = requests.get(site).json()  # reads data from the url getUpdates
            if (data['result'] != []):
                lastMsg = len(data['result']) - 1
                updateId = data['result'][lastMsg]['update_id']
                chatid = str(data['result'][lastMsg]['message']['chat']['id'])  # reads chat ID
                if (updateId != updateIdSave):  # compares update ID
                    text = data['result'][lastMsg]['message']['text']  # reads what they have sent
                    requests.get(f'https://api.telegram.org/bot{self.botToken}/getUpdates?offset=' + str(updateId))
                    break
                elif waitingTime < datetime.now():
                    text = ''
                    break
        return text

    def sendText(self, message):
        URL=f"https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={self.chatid}&text={message}"
        requests.get(URL)

    def sendImage(self, directory):
        try:
            imgpath = {'photo': open(directory, 'rb')}
            requests.post(
                f'https://api.telegram.org/bot{self.botToken}/sendPhoto?chat_id={self.chatid}',
                files=imgpath)  # Sending Automated Image
            print("Image Sent")
        except:
            print("Failed to send Image")
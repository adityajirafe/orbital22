class Job_Item:
    def __init__(self, chat_id, message, Job, coin = "", favoured_trade = ""):
        self.chat_id = chat_id
        self.message = message
        self.job = Job
        self.coin = coin
        self.favoured_trade = favoured_trade
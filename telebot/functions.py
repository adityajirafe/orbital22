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

def handle_trade(job_item, bot):
    bot.sendText(
        "Trade executed",
        job_item.chat_id
    )
    print(job_item.message)
    return 

def handle_no_trade(job_item, bot):
    bot.sendText(
        "Trade NOT executed",
        job_item.chat_id
    )
    print(job_item.message)
    return 
import time
import schedule
import requests
import telegram


class Messenger():
    def __init__(self, token, channel_name):
        self.url = 'https://api.telegram.org/bot'
        self.token = token
        self.chat_id = None
        self.channel_name = channel_name
        self.bot = telegram.Bot(token=self.token)

    def send_message(self, message):
        self.bot.send_message(chat_id=f'@{self.channel_name}', text=message)

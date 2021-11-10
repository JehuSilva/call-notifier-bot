import os
import telegram

from backend.logger import logger
from static.message import notification
from telegram.error import RetryAfter, BadRequest


class Messenger():
    def __init__(self):
        self.url = 'https://api.telegram.org/bot'

    def get_bot_credentials(self, destination):
        '''
        Returns the bot credentials for a given destination
        '''
        return {
            'Available': {
                'token': os.environ.get('PIZZAL_TOKEN'),
                'channel_id': os.environ.get('PIZZAL_CHANNEL_ID')
            },
            'Mago Magum': {
                'token': os.environ.get('MAGO_MAGUM_TOKEN'),
                'channel_id': os.environ.get('MAGO_MAGUM_CHANNEL_ID')
            },
            'Fisiodinamic': {
                'token': os.environ.get('FISIODINAMIC_TOKEN'),
                'channel_id': os.environ.get('FISIODINAMIC_CHANNEL_ID')
            },

        }.get(destination, None)

    def send_messages(self, messages):
        ''' This functions will send the messages by every bot'''
        # Reverse in order to send the last message first
        messages.reverse()

        # Send the messages one by one
        for message in messages:
            try:
                keys = self.get_bot_credentials(message['destination'])
                if keys is None:
                    continue
                bot = telegram.Bot(token=keys['token'])
                logger.info(f'Sending message to {message["destination"]}')
                bot.send_message(
                    chat_id=keys['channel_id'],
                    text=notification.format(**message),
                    parse_mode=telegram.ParseMode.HTML
                )
            except RetryAfter:
                logger.error(
                    'To many messages sent. '
                    'The missing messages will be sent in the next execution'
                )
            except BadRequest as e:
                logger.error(
                    f'The bot is not authorized to send messages to the channel: {message["destination"]}'
                )
                logger.error(e)

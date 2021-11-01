import os
import json
import pandas as pd

from backend.callpicker import CallPicker
from backend.messenger import Messenger
from static.message import notification


import logging
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHANNEL_NAME = os.environ.get('CHANNEL_NAME')

if __name__ == '__main__':
    '''
    This is the main entry point for the application.
    '''
    register = CallPicker()
    notifier = Messenger(TELEGRAM_TOKEN, CHANNEL_NAME)

    calls_row = register.get_calls()
    calls_df = pd.DataFrame(calls_row)
    calls_df.to_csv('temp/calls.csv', index=False)

    # notifier.send_message(notification.format(
    #     prety_date='2021', date='2021',
    #     who_answered='some people', customer='customer'
    # ))

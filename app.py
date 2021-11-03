from backend.db import DataBase
from backend.logger import logger
from backend.utils import Transformer
from backend.messenger import Messenger
from backend.callpicker import CallPicker


REGISTER_SIZE = 20

if __name__ == '__main__':
    '''
    This is the main entry point for the application.
    '''
    logger.info('Starting application')
    callpicker = CallPicker()
    database = DataBase()
    transformer = Transformer()
    notifier = Messenger()

    last_logs_df = transformer.get_last_logs(
        callpicker.get_calls(), size=REGISTER_SIZE
    )
    stored_logs = database.get_stored_logs(size=REGISTER_SIZE)
    new_calls_df = transformer.split_new_logs(
        last_logs_df, stored_logs
    )
    if len(new_calls_df):
        logger.info('New calls found! Sending messages')
        messages = transformer.get_messages_dict(new_calls_df)
        notifier.send_messages(messages)
        logger.info('Updating database')
        database.save_last_logs(new_calls_df)
    else:
        logger.info('No new calls found')
    logger.info('Done!')

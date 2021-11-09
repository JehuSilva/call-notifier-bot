import time
from backend.db import DataBase
from backend.logger import logger
from backend.utils import Utils
from backend.messenger import Messenger
from backend.callpicker import CallPicker


def main(event, context):
    '''
    This is the main entry point for the application.
    '''
    SIZE = 10  # Number of calls to be picked
    # Initialize the database usefull objects
    start_time = time.time()
    logger.info('Starting application')
    callpicker = CallPicker()
    database = DataBase(schema='pizzall')
    utils = Utils()
    notifier = Messenger()

    # Updating tables in de database deppending on the time of the day
    if utils.is_time_in_range(when='morning'):
        logger.info('It is morning. Deleting old historical calls')
        database.delete_old_rows(table='calls_history')
        database.delete_2_days_rows(table='callpicks')
    if utils.is_time_in_range(when='afternoon'):
        last_calls = utils.format_to_bq(callpicker.get_calls(size=50, page=1))
        database.upload_rows('calls_history', last_calls)
    if utils.is_time_in_range(when='night'):
        last_calls = utils.format_to_bq(callpicker.get_calls(size=50, page=1))
        database.upload_rows('calls_history', last_calls)

    # Fetching the last ten calls from callpicker and
    # find the ones that are not registered in the database
    last_calls = utils.format_to_bq(callpicker.get_calls(size=SIZE))
    saved_calls = database.get_saved_calls(table='callpicks', size=SIZE)
    new_calls = utils.split_new_calls(last_calls, saved_calls)

    # Register the new calls in the database and
    # send the notifications to the users
    if len(new_calls) > 0:
        logger.info('New calls found! Sending notifications')
        notifier.send_messages(utils.format_to_telegram(new_calls))
        database.upload_rows('callpicks', new_calls)
    else:
        logger.info('No new calls found')
    logger.info(
        'Done! Execution time: %.3f seconds' % (time.time() - start_time)
    )


if __name__ == '__main__':
    main(None, None)

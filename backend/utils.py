import pytz
import datetime


class Utils:
    '''
    This class helps to format the datasets
    in order to interact with the database
    '''

    def __init__(self):
        pass

    def split_new_calls(self, rows, stored_ids):
        '''
        Returns only the new calls not stored in bq
        '''
        return [row for row in rows if row['id'] not in stored_ids]

    def format_to_bq(self, rows):
        '''
        Formats the rows according the pizzal.callpicks format.
        '''
        return [
            {
                'status': row['status'],
                'destination': row['destination'],
                'redirection_type': row['redirection_type'],
                'player': row['player'],
                'duration': int(row['duration']) if row['duration'] != '-' else 0,
                'returned': bool(row['returned']),
                'person_name': row['person_name'],
                'caller_id': row['caller_id'],
                'tagged': bool(row['tagged']),
                'trunk': row['trunk'],
                'rating': row['rating'],
                'date': row['date'],
                'pretty_date': row['pretty_date'],
                'uniqueid': row['uniqueid'],
                'id': int(row['id']),
                'clean_caller_id': row['clean_caller_id'],
                'has_notes': bool(row['has_notes']),
                'trunk_description': row['trunk_description'],
                'update_time': datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            } for row in rows
        ]

    def split_date_and_time(self, date_time):
        '''
        Splits a datetime string in format '%Y-%m-%d %H:%M:%S'
        to date and time
        '''
        date, time = date_time.split(' ')
        return date, time

    def translate_status(self, status):
        '''
        Translate the status to spanish
        '''
        return {
            'Self_service': '<b>Status</b>: <i>Autoservicio</i> \U0001F535 ',
            'Redirected': '<b>Status</b>: <i>Redireccionada</i> \U0001F7E2 ',
            'Lost': '<b>Status</b>: <i>Perdida</i> \U0001F534 ',
            'Voicemail': '<b>Status</b>: <i>Mensaje de voz</i> \U0001F7E0 ',
        }[status]

    def get_destination(self, destination):
        '''
        Gets the destination leyend acording to the
        new tag received
        '''
        return {
            'Available': 'Pizzall Santa Rosa',
            'Mago Magum': 'Mago Magun',
            'Fisiodinamic': 'Fisiodinamic',
            'Tacozole': 'Tacozole',
        }.get(destination, None)

    def format_to_telegram(self, rows):
        '''
        Returns a list of dicts with the information
        the telegram message needs
        '''
        return [
            {
                'status': self.translate_status(row['status']),
                'company_phone': row['trunk'],
                'customer': row['caller_id'],
                'who_answered': row['destination'],
                'date': row['date'].split(' ')[0],
                'time': row['date'].split(' ')[1],
                'pretty_date': row['pretty_date'],
                'destination': row['trunk_description'],
                'destination_details': self.get_destination(
                    row['trunk_description']
                )
            } for row in rows
        ]

    def is_time_in_range(self, when='morning'):
        '''Returns whether current is in the range '''
        tz = pytz.timezone('America/Mexico_City')
        if when == 'morning':
            start = datetime.time(9, 0, 0)
            end = datetime.time(9, 0, 30)
        if when == 'afternoon':
            start = datetime.time(15, 15, 0)
            end = datetime.time(15, 15, 30)
        if when == 'night':
            start = datetime.time(23, 58, 0)
            end = datetime.time(23, 58, 30)
        return start <= datetime.datetime.now(tz).time() <= end

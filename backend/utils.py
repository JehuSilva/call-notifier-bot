import pandas as pd


class Transformer:
    '''
    This class helps to format the datasets
    in order to interact with the database
    '''

    def __init__(self):
        pass

    def get_last_logs(self, rows, size=15):
        '''
        Returns a dataframe with the logs
        '''
        return pd.DataFrame(
            [Model(row).get_keys() for row in rows]
        ).sort_values(by='date', ascending=False)[0:size]

    def split_new_logs(self, df1, df2):
        '''
        Returns the difference between both dataframes
        '''
        if df2 is not None:
            diff_df = df1.merge(df2, left_on='id', right_on='id', how='inner')
            return df1[~df1['id'].isin(diff_df['id'])].drop_duplicates()
        else:
            return df1

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
            'Self_service': '\U0001F535 <b>Status</b>: <i>Autoservicio</i> ',
            'Redirected': '\U0001F7E2 <b>Status</b>: <i>Redireccionada</i> ',
            'Lost': '\U0001F534 <b>Status</b>: <i>Perdida</i>',
            'Voicemail': '\U0001F7E0 <b>Status</b>: <i>Mensaje de voz</i>',
        }[status]

    def get_destination(self, destination):
        '''
        Gets the destination leyend acording to the
        new tag received
        '''
        return {
            'Available': 'Pizzal Santa Rosa',
            'Mago Magum': 'Mago Magun',
            'Fisiodinamic': 'Fisiodinamic',
        }[destination]

    def get_messages_dict(self, df):
        '''
        Returns a list of dicts with the information
        the telegram message needs
        '''
        def converter(row):
            date, time = self.split_date_and_time(row['date'])
            return {
                'status': self.translate_status(row['status']),
                'company_phone': row['telephone_number'],
                'customer': row['customer'],
                'who_answered': row['who_answered'],
                'date': date,
                'time': time,
                'pretty_date': row['pretty_date'],
                'destination': row['destination_description'],
                'destination_details': self.get_destination(
                    row['destination_description']
                )
            }
        return df.apply(converter, axis=1).tolist()


class Model():
    def __init__(self, row):
        self.status = row['status']  # 'available' or 'busy'
        self.destination = row['destination']  # who answered
        self.redirection_type = row['redirection_type']
        self.player = row['player'],
        self.duration = row['duration']  # duration
        self.returned = row['returned']
        self.person_name = row['person_name']
        self.caller_id = row['caller_id']  # customer
        self.tagged = row['tagged']
        self.trunk = row['trunk']  # TELEPHONE NUMBER
        self.rating = row['rating']
        self.date = row['date']  # date
        self.pretty_date = row['pretty_date']  # pretty_date
        self.uniqueid = row['uniqueid']
        self.id = row['id']
        self.clean_caller_id = row['clean_caller_id']
        self.has_notes = row['has_notes']
        self.trunk_description = row['trunk_description']

    def get_keys(self):
        return {
            'id': self.id,
            'status': self.status,
            'telephone_number': self.trunk,
            'duration': self.duration,
            'customer': self.caller_id,
            'who_answered': self.destination,
            'date': self.date,
            'pretty_date': self.pretty_date,
            'destination_description': self.trunk_description,
        }

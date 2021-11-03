import sqlite3
import pandas as pd
from backend.logger import logger
from pandas.io.sql import DatabaseError


class DataBase():
    def __init__(self):
        self.connection = None
        # self.create_table()

    def get_connection(self):
        '''
        Create a connection to the database
        '''
        self.connection = None
        try:
            self.connection = sqlite3.connect('callpicker.db')
        except Exception as e:
            print(e)
        return self.connection

    def save_last_logs(self, df):
        '''
        Inserts a dataframe into the call logs table
        '''
        with self.get_connection() as cnx:
            df.to_sql(name='call_logs', con=cnx, if_exists='append')

    def delete_df(self):
        '''
        Delets the entire call_logs table
        '''
        with self.get_connection() as cnx:
            cursor = cnx.cursor()
            cursor.execute('DELETE FROM call_logs;')

    def get_stored_logs(self, size=15):
        '''
        Reads the current last 20 stored
        '''
        df = None
        with self.get_connection() as cnx:
            try:
                df = pd.read_sql(f'''
                    SELECT DISTINCT * FROM call_logs 
                    ORDER BY date DESC
                    LIMIT {size};
                ''', con=cnx)[[
                    'id', 'status', 'telephone_number', 'duration',
                    'customer', 'who_answered', 'date', 'pretty_date',
                    'destination_description'
                ]]
            except DatabaseError:
                logger.error('Table not found, create table.')
                df = None
        return df

    def get_difference(self, df1, df2):
        '''
        Returns the difference between both dataframes
        '''
        diff_df = pd.merge(df1, df2, how='outer', indicator='Exist')
        return diff_df.loc[diff_df['Exist'] != 'both'].loc[
            :, diff_df.columns != 'Exist'
        ]

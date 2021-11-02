import os
import pickle
import logging
import pandas as pd

logging.basicConfig()
logger = logging.getLogger('storage')
logger.setLevel(logging.INFO)


class FileManager():
    def __init__(self, directory='temp/'):
        self.directory = directory

    def save_dataframe(self, df, dataset_name):
        '''
        Saves a given dataset to a pickle file
        '''
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        except FileExistsError:
            pass
        with open(f'{self.directory}/{dataset_name}.pkl', 'wb') as file:
            pickle.dump(df, file)
            logger.info('File saved')

    def read_dataframe(self, dataset_name):
        '''
        Loads dataset from local files
        '''
        try:
            with open(f'{self.directory}/{dataset_name}.pkl', 'rb') as file:
                df = pickle.load(file)
                logger.info('Found a file... Loaded!')
                return df
        except FileNotFoundError:
            raise Exception('File not found')

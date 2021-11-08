from backend.logger import logger

import json
from google.cloud import bigquery as bq
from google.oauth2 import service_account
from google.api_core.exceptions import BadRequest, NotFound

with open('/home/jehu/jehu/pizzal/bq_credentials.json') as f:
    json_credentials = json.load(f)

credentials = service_account.Credentials.from_service_account_info(
    json_credentials
)


class DataBase():
    '''
    Functions to transfer data from the applications and the database
    '''

    def __init__(self, project='promobot-mcbftp', schema='pizzall'):
        self.schema = schema
        self.client = bq.Client(project=project, credentials=credentials)

    def delete_old_rows(self, table='calls_history'):
        '''
        Delets old calls logs
        '''
        logger.info(f'Deleting old calls in {self.schema}.{table}')
        self.client.query(f'''
            DELETE {self.schema}.{table} t
            WHERE (t.id, t.update_time ) 
            NOT IN (
                SELECT (id, MAX(update_time))
                FROM {self.schema}.{table} 
                GROUP BY id
            );''')

    def delete_2_days_rows(self, table='callpicks'):
        '''
        Deletes calls of two days and past
        '''
        logger.info(f'Deleting two days past calls in {self.schema}.{table}')
        self.client.query(f'''
            DELETE {self.schema}.{table} t
            WHERE (t.id, t.update_time)
            NOT IN (
                SELECT   (id, MAX(update_time)) 
                FROM {self.schema}.{table}
                WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
                GROUP BY id
            );''')

    def get_saved_calls(self, table='callpicks', size=15):
        '''
        Returns te last {size} calls from the given table
        '''
        try:
            return [row[0] for row in self.client.query(f'''
                WITH latest AS (
                SELECT id, MAX(update_time) t
                    FROM {self.schema}.{table}
                    GROUP BY id
                ) SELECT p.id FROM {self.schema}.{table} p
                INNER JOIN latest 
                ON p.id = latest.id AND p.update_time = latest.t
                ORDER BY p.date DESC
                LIMIT {size};
            ''')]
        except NotFound:
            raise Exception(
                'Table in bigquery not exists. Issue in the worflow'
            )
        except Exception as e:
            logger.error('Couldn\'t execute the query')
            raise e

    def upload_rows(self, table, rows):
        try:
            logger.info(f'Uploading {len(rows)} rows to {table}')
            table_fullname = f'promobot-mcbftp.{self.schema}.{table}'
            job = self.client.insert_rows_json(table_fullname, rows)
            if job:
                raise Exception(
                    f'An error occurred while uploading rows to {self.schema}.{table}'
                    f'job: {job}'
                )
        except NotFound:
            logger.error(
                f'Couldn\'t update table. {self.schema}.{table} not found! '
                f'{len(rows)} rows affected'
            )

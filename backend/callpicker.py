
import requests
from backend.logger import logger
from json.decoder import JSONDecodeError

import http.client as client
client._MAXHEADERS = 1000


class CallPicker():
    '''
    This class is used to get the calls from the CallPicker API.
    '''

    def __init__(self):
        self.URL = 'https://admin.callpicker.com/call_details/get_call_details_page/'
        self.HEADERS = {
            'authority': 'admin.callpicker.com',
            'accept': 'application/json',
        }
        self.COOKIES = {
            '_ga': 'GA1.2.951352925.1634611210',
            'hblid': '367BWuWIfReTT94z1z9T10UFKrj7FBXa',
            'olfsk': 'olfsk12517325553219538',
            '_gid': 'GA1.2.1242366130.1636257684',
            '_okdetect': '%7B%22token%22%3A%2216362576848420%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D',
            '_ok': '5509-639-10-9611',
            'wcsid': '8z9b9vw6zd6WkvzC1z9T10VOXF2bBBaK',
            '_okbk': 'cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1636299774488%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C',
            '_gat': '1',
            'Callpicker_admin': 'lolaj4hammlp4jf9mopi1momk4',
            '_oklv': '1636311777410%2C8z9b9vw6zd6WkvzC1z9T10VOXF2bBBaK',
        }

    def get_calls(self, size=50, page=1):
        '''
        This function returns a list of calls from the CallPicker API.
        '''
        self.PARAMS = {
            'referrerPolicy': 'strict-origin-when-cross-origin',
            'page': page,
        }
        try:
            logger.info('Fetching last calls from CallPicker')
            return requests.get(
                self.URL, headers=self.HEADERS, cookies=self.COOKIES, params=self.PARAMS
            ).json()['payload'][:size]
        except JSONDecodeError:
            logger.error('JSONDecodeError')

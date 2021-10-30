

import requests
import http.client  as client
client._MAXHEADERS = 1000

class CallPicker():
    def __init__(self):
        self.URL = 'https://admin.callpicker.com/call_details/get_call_details_page/'
        self.HEADERS = {
          'authority': 'admin.callpicker.com',  
          'accept': 'application/json',
        }
        self.COOKIES= {
          '_ga':'GA1.2.951352925.1634611210',
          'hblid':'367BWuWIfReTT94z1z9T10UFKrj7FBXa',
          'olfsk':'olfsk12517325553219538',
          'Callpicker_admin':'6bv3vi201gnjpuojsfo7v304b5',
          '_gid':'GA1.2.1609770453.1635545453',
          '_gat':'1',
          'wcsid':'kxp4OhXlzifJTUir1z9T10UbajKB2FBF',
          '_oklv':'1635545453386%2Ckxp4OhXlzifJTUir1z9T10UbajKB2FBF',
          '_okdetect':'%7B%22token%22%3A%2216355454535550%22%2C%22proto%22%3A%22about%3A%22%2C%22host%22%3A%22%22%7D',
          '_ok':'5509-639-10-9611',
          '_okbk':'cd5%3Davailable%2Ccd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1635545453795%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C',
        }
        self.PARAMS = {
        'referrerPolicy': 'strict-origin-when-cross-origin',
        'page': 1,

        }
    def get_calls(self):
        response = requests.get(
            self.URL, headers=self.HEADERS, cookies=self.COOKIES, params=self.PARAMS
        ).json()['payload']
        return [Model(row).get_keys() for row in response]



class Model():
  def __init__(self, row):
    self.status=row['status'] # 'available' or 'busy'
    self.destination=row['destination'] # who answered
    self.redirection_type=row['redirection_type']
    self.player = row['player'],
    self.duration=row['duration'] #duration
    self.returned=row['returned']
    self.person_name=row['person_name']
    self.caller_id=row['caller_id'] # customer
    self.tagged=row['tagged']
    self.trunk=row['trunk'] #TELEPHONE NUMBER
    self.rating=row['rating']
    self.date=row['date'] # date
    self.pretty_date=row['pretty_date'] # pretty_date
    self.uniqueid=row['uniqueid']
    self.id=row['id']
    self.clean_caller_id=row['clean_caller_id']
    self.has_notes=row['has_notes']
    self.trunk_description=row['trunk_description']

  def get_keys(self):
    return {
      'status': self.status,
      'telephone_number': self.trunk,
      'duration': self.duration,
      'customer': self.caller_id,
      'who_anwered': self.destination,
      'date': self.date,
      'pretty_date': self.pretty_date,
      'destination_description': self.trunk_description,
    }
import json
import requests
import os
import http.client  as client# or http.client if you're on Python 3
client._MAXHEADERS = 1000


url = 'https://admin.callpicker.com/call_details/get_call_details_page/'
headers = {
  # 'sec-ch-ua': '\'Chromium\';v=\'92\', \' Not A;Brand\';v=\'99\', \'Google Chrome\';v=\'92\'',
  'authority': 'admin.callpicker.com',
  'accept': 'application/json',
  'sec-ch-ua-mobile': '?0',
  # 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
  # 'content-type': 'application/x-www-form-urlencoded',
  # 'origin': 'https://admin.callpicker.com',
  # 'sec-fetch-site': 'same-origin',
  # 'sec-fetch-mode': 'cors',
  # 'sec-fetch-dest': 'empty',
  # 'referer': 'https://admin.callpicker.com/call_details',
  # 'accept-language': 'en-MX,en;q=0.9,es-MX;q=0.8,es;q=0.7,en-US;q=0.6',
}
cookies= {
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
params = {
# 'referrer': 'https://admin.callpicker.com/call_details',
'referrerPolicy': 'strict-origin-when-cross-origin',
'page': 1,
# 'page=1&sort%5Bkey%5D=&sort%5Border%5D=false',
# 'method': 'POST',
# 'mode': 'cors',
# 'credentials': 'include',
# page=1
# sort%5Bkey%5D=&sort%5Border%5D=false',
}
  
response = requests.get(url=url,headers=headers, params=params, cookies=cookies)
# print in json format the current response
# print(response.text)
print(json.dumps(response.json(), indent=4, sort_keys=True))


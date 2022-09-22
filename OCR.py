import requests
import uuid
import time
import json

api_url ='https://gnqvoohdeh.apigw.ntruss.com/custom/v1/17501/d217bed6412bddad99689e8ed903afc039d6475de2a7f2ff116768c96b7b3b30/general'
secret_key = 'bExwVkJpVG9VVVhteW9oRmNSWExyWHNHdGNlRlNDa0c='
image_file = '컨테이너.png'

request_json = {
    'images': [
        {
            'format': 'png',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))
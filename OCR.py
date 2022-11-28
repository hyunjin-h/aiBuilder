import requests
import uuid
import time
import json
def ocr(imgFile):
    global ocr_res
    api_url ='https://nufmp03pym.apigw.ntruss.com/custom/v1/19385/a5729de6f4b4e7817359cceb25803b260165d7ffa53f0cb3e68cca3ea1f004ac/general'
    secret_key = 'R0hQWUF5Y0lwbHJBVHBaTGdVWHZzTXd3R2Rza0dMQXU='
    image_file = imgFile

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

    ocr_res = json.loads(response.text)
    print(ocr_res)
    data = ocr_res['images'][0]['fields']

    ocr_res = ' '.join([_['inferText'] for _ in data])
    print(ocr_res)


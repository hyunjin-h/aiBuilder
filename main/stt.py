import sys
import json
import requests
def stt(sound):
    global stt_res
    client_id = "mmmau3h9mh"
    client_secret = "019qpb0hJ0ttjUAFjNQwx1ZiRVoj2hxyPBNffoKU"
    lang = "Eng" # 언어 코드 ( Kor, Jpn, Eng, Chn )
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang

    data = open(f'{sound}', 'rb')
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url,  data=data, headers=headers)
    rescode = response.status_code
    if(rescode == 200):
        stt_res = json.loads(response.text)
        stt_res = stt_res['text']
        print(stt_res)

    else:
        print("Error : " + response.text)

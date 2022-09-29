import os
import sys
import requests
import json

def face(imgFile):
    global face_result
    client_id = "pficodqpxs"
    client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
    url = "https://naveropenapi.apigw.ntruss.com/vision/v1/face"
    files = {'image': open(imgFile, 'rb')}
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if (rescode == 200):
                fac_res = json.loads(response.text)
                fac_gender='예측 성별: '+str(fac_res['faces'][0]['gender']['value'])+'\n'
                fac_age='예측 나이: '+str(fac_res['faces'][0]['age']['value'])+'\n'
                fac_emo='예측 감정: '+str(fac_res['faces'][0]['emotion']['value'])+'\n'
                face_result=fac_gender+fac_age+fac_emo

    else:
        print("Error Code:" + rescode)



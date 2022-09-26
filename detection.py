import os
import sys
import requests
import json
def object_detect(imgFile):
    global obj_res
    client_id = "pficodqpxs"
    client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
    url = "https://naveropenapi.apigw.ntruss.com/vision-obj/v1/detect" #객체 인식
    files = {'image': open(f'{imgFile}', 'rb')}
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        obj_res = json.loads(response.text)
        obj_res = obj_res['predictions'][0]['detection_names']

    else:
        print("Error Code:" + rescode)
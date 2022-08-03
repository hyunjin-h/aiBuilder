import os
import sys
import requests
client_id = "pficodqpxs"
client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
url = "https://naveropenapi.apigw.ntruss.com/vision-obj/v1/detect" #객체 인식
files = {'image': open('image/image.jpg', 'rb')}
headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
if(rescode==200):
    print (response.text)
else:
    print("Error Code:" + rescode)
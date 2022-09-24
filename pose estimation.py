import os
import sys
import requests
client_id = "pficodqpxs"
client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
url = "https://naveropenapi.apigw.ntruss.com/vision-pose/v1/estimate" # 사람 인식
files = {'image': open('./image/image.jpg', 'rb')}
headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
response = requests.post(url,  files=files, headers=headers)
rescode = response.status_code
res=response.text

if(rescode==200):
    print (res)

else:
    print("Error Code:" + rescode)


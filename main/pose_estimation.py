import os
import sys
import requests
def pose_estimation(imgFile):
    global pose
    client_id = "mmmau3h9mh"
    client_secret = "019qpb0hJ0ttjUAFjNQwx1ZiRVoj2hxyPBNffoKU"
    url = "https://naveropenapi.apigw.ntruss.com/vision-pose/v1/estimate" # 사람 인식
    files = {'image': open(imgFile, 'rb')}
    headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    res=response.text

    if(rescode==200):
        pose=res
        print (res)

    else:
        print("Error Code:" + rescode)


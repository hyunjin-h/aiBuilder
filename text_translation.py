import os
import sys
import urllib.request
import json
def trans(text,source,target):
    global trans_res
    client_id = "88nlvtm8gq"
    client_secret = "gLqWxSUK0rdeT3h3PW74nqMDB02Q0b3q6q8LVGsK"

    encText = urllib.parse.quote(text)
    data = "source="+source+"&target="+target+"&text=" + encText #여기에서 언어를 바꾸면 될듯 조건문 사용해서
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        trans_res = response_body.decode('utf-8')
        trans_res = json.loads(trans_res)
        trans_res = trans_res['message']['result']['translatedText']

        print(trans_res)

    else:
        print("Error Code:" + rescode)

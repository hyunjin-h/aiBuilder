import os
import sys
import urllib.request

def tts(text,lang):
    global sound_path
    if lang == 'ko':
        voice = 'nara'
    elif lang == 'en':
        voice = 'clara'
    elif lang == 'ja':
        voice = 'nnaomi'

    client_id = "pficodqpxs"
    client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
    encText = urllib.parse.quote(text)
    data = "speaker="+voice+"&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        path='soundFiles/output.mp3'
        uniq=1
        while os.path.exists(path):  # 동일한 파일명이 존재할 때
            path = 'soundFiles/output(%d).mp3' % (uniq)  # 파일명(1) 파일명(2)...
            uniq += 1
        with open(path, 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
    sound_path=path
import urllib.request
import json


def detect_lang(text):
        global lang
        client_id = "88nlvtm8gq"
        client_secret = "gLqWxSUK0rdeT3h3PW74nqMDB02Q0b3q6q8LVGsK"
        encQuery = urllib.parse.quote(text)
        data = "query=" + encQuery
        url = "https://naveropenapi.apigw.ntruss.com/langs/v1/dect"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            lang = response_body.decode('utf-8')
            lang = json.loads(lang)
            lang = lang['langCode']
            print(lang)
        else:
            print("Error Code:" + rescode)

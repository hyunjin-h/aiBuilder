import requests
from requests_toolbelt import MultipartEncoder
import uuid
import json
import base64

client_id="mmmau3h9mh"
client_secret="019qpb0hJ0ttjUAFjNQwx1ZiRVoj2hxyPBNffoKU"

data = {
  'source': 'en', #source랑 target 바꿔주기
  'target': 'ko',
  'image': ('송장_한.png', open('송장.png', 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
} #여기에서 파일이름이랑 경로 써주면 될듯!!!
m = MultipartEncoder(data, boundary=uuid.uuid4())

headers = {
  "Content-Type": m.content_type,
  "X-NCP-APIGW-API-KEY-ID": client_id,
  "X-NCP-APIGW-API-KEY": client_secret
}

url = " https://naveropenapi.apigw.ntruss.com/image-to-image/v1/translate"
res = requests.post(url, headers=headers, data=m.to_string())
print(res.text)

# renderedImage -> 이미지 파일로 출력
resObj = json.loads(res.text)
imageStr = resObj.get("data").get("renderedImage")
imgdata = base64.b64decode(imageStr)

filename = 'a_translated.png'
with open(filename, 'wb') as f:
    f.write(imgdata)

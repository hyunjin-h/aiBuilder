import requests
import json

encText='mountain'
url='http://175.45.195.35:5000/model/'+encText
r=requests.get(url)
r=r.content

save_file = open("image/dalle.png", "wb")
save_file.write(r)
save_file.close()


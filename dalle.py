import requests
import json
def dalle(text):

    encText=text
    url='http://175.45.193.155:5000/model/'+encText
    r=requests.get(url)
    r=r.content

    save_file = open("image/dalle.png", "wb")
    save_file.write(r)
    save_file.close()




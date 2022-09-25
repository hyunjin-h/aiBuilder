from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import urllib.request
import json

form_text=uic.loadUiType('_uiFiles/textInput.ui')[0]

class TextDialog(QDialog,form_text):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self):
        super(TextDialog, self).__init__()
        self.initUI()
        self.show()

        self.text = ""
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.setupUi(self)
        self.textCheck.clicked.connect(self.quit_text)

    def quit_text(self):

        self.text = str(self.textEdit.toPlainText())
        self.detect_lang()
        self.close()


    def detect_lang(self):
        global lang
        client_id = "pficodqpxs"
        client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"
        encQuery = urllib.parse.quote(self.text)
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






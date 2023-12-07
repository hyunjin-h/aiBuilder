from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

form_lang=uic.loadUiType('_uiFiles/langselect.ui')[0]

class LangDialog(QDialog,form_lang):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self):
        super(LangDialog, self).__init__()
        self.initUI()
        self.show()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)


    def initUI(self):
        self.setupUi(self)
        self.langCheck.clicked.connect(self.quit_lang)

    def quit_lang(self):
        global mainlang
        mainlang = self.selectLang.currentText()
        if mainlang == '한국어':
            mainlang = 'ko'
            print(mainlang)
        elif mainlang == '영어':
            mainlang = 'en'
            print(mainlang)
        elif mainlang == '일본어':
            mainlang = 'ja'
            print(mainlang)
        elif mainlang == '중국어-간체':
            mainlang = 'zh-CN'
            print(mainlang)
        elif mainlang == '중국어-번체':
            mainlang = 'zh-TW'
            print(mainlang)
        elif mainlang == '베트남어':
            mainlang = 'vi'
            print(mainlang)
        elif mainlang == '인도네시아어':
            mainlang = 'id'
            print(mainlang)
        elif mainlang == '태국어':
            mainlang = 'th'
            print(mainlang)
        elif mainlang == '독일어':
            mainlang = 'de'
            print(mainlang)
        elif mainlang == '러시아어':
            mainlang = 'ru'
            print(mainlang)
        elif mainlang == '스페인어':
            mainlang = 'es'
            print(mainlang)
        elif mainlang == '이탈리아어':
            mainlang = 'it'
            print(mainlang)
        elif mainlang == '프랑스어':
            mainlang = 'fr'
            print(mainlang)

        self.accept()

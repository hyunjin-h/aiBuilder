from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

form_lang=uic.loadUiType('_uiFiles/objectOut.ui')[0]

class odDialog(QDialog,form_lang):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self):
        super(odDialog, self).__init__()
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

        self.accept()

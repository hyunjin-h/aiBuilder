from PyQt5 import uic
from PyQt5.QtWidgets import *


class TextDialog(QDialog):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self, parent):
        super(TextDialog, self).__init__(parent)
        text_ui = '_uiFiles/textInput.ui'
        uic.loadUi(text_ui, self)
        global text
        self.show()
        self.textCheck.clicked.connect(self.quit_text)

    def quit_text(self):
        # self.detect_lang()
        text = str(self.textEdit.toPlainText())
        print(text)
        self.accept()


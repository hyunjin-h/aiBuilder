from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class TextDialog(QDialog):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self, parent):
        super(TextDialog, self).__init__(parent)
        text_ui = '_uiFiles/textInput.ui'
        uic.loadUi(text_ui, self)
        self.show()

        self.textCheck.clicked.connect(self.quit_text)

    def quit_text(self):
        global text_input
        text_input = self.textEdit.toPlainText()
        text_input = str(text_input)
        print(text_input)
        # self.detect_lang()
        self.accept()


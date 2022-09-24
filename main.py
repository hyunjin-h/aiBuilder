import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic,QtCore
import input_text, RecorD
from input_text import TextDialog

form_class = uic.loadUiType("_uiFiles/mainPage.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.mainList.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        self.runBtn.clicked.connect(self.runModel)

        self.fileList.setSpacing(5)
        self.inputList.setSpacing(5)
        self.modelList.setSpacing(5)
        self.text=""

    def chkItemDoubleClicked(self):
        rowNum=self.mainList.currentRow()
        rowText=self.mainList.currentItem().text()
        print(str(rowNum) + " : " + rowText)


        if(rowText=='text'):
            self.inputTxt=TextDialog()
            self.inputTxt.exec()
            self.text=self.inputTxt.text
            self.show()



        elif(rowText=='image'):
            self.fileopen()
        elif(rowText=='sound'):
            self.fileopen()
        elif(rowText=='camera'):
            os.system('cam.py')
            try:
                inputImg='image/input_photo.jpg'
            except:
                pass
        elif(rowText=='mic'):
            app = RecorD.RecGui()
            app.mainloop()

        elif(rowText=='TTS'):
            print(rowText)
        elif(rowText=='STT'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)

    def runModel(self):
        rowNum=self.mainList.currentRow()


    def fileopen(self):
        global filename
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        global filepath
        filepath = f'{filename[0]}'
        print(filepath)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


import os
import sys
import webbrowser

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic,QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import  RecorD
from input_text import TextDialog
import tts, stt

form_class = uic.loadUiType("_uiFiles/mainPage.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.txt=""
        self.fileDir=''

    def initUI(self):
        self.mainList.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        self.runBtn.clicked.connect(self.runModel)
        self.resetBtn.clicked.connect(self.clear)
        
        self.fileList.setSpacing(8)
        self.inputList.setSpacing(8)
        self.modelList.setSpacing(8)
        self.mainList.setSpacing(8)


    def chkItemDoubleClicked(self):
        rowNum=self.mainList.currentRow()
        rowText=self.mainList.currentItem().text()
        print(str(rowNum) + " : " + rowText)


        if(rowText=='text'):
            self.inputTxt=TextDialog()
            self.inputTxt.exec()
            self.txt=self.inputTxt.text
            print(self.txt)
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
            RecorD.main()
            filepath = RecorD.filename
            specialChars = "\\"
            for specialChar in specialChars:
                filepath = filepath.replace(specialChar, '/')
                print(filepath)
            self.fileDir=filepath

        elif(rowText=='TTS'):
            print(rowText)
        elif(rowText=='STT'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)

    def runModel(self):
        lw = self.mainList
        last=lw.count()-1
        print(last)
        items = [lw.item(x).text() for x in range(lw.count())]
        for i in items:
            if(i=='TTS'):
                tts.tts(self.txt)
                self.fileDir='soundFiles/output.mp3'
                if(lw.item(last).text()=='TTS'):
                    btnPlay=QPushButton("play")
                    btnPlay.setMaximumWidth(250)
                    btnPlay.setMinimumHeight(250)
                    self.plyOut.addWidget(btnPlay)
                    btnPlay.clicked.connect(lambda :self.play())
                    def play():
                        webbrowser.open(self.fileDir)


            elif(i=='STT'):
                stt.stt(self.fileDir)
                print(stt.stt_res)
            elif(i=='번역'):
                print(items[i + 1])
            elif(i=='이미지번역'):
                print(items[i + 1])
            elif(i=='OCR'):
                print(items[i + 1])
            elif(i=='Object Detection'):
                print(items[i + 1])
            elif(i=='Image Generation'):
                print(items[i + 1])

            else:
                pass


    def clear(self):
        self.txt = ''
        self.fileDir = ''
        self.mainList.clear()



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


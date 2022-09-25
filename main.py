import os
import sys
import pygame


from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic,QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import  RecorD
from input_text import TextDialog
from select_lang import LangDialog
import tts, stt,text_translation,select_lang,input_text

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
            self.source=input_text.lang

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

        elif(rowText=='번역'):
            self.langD = LangDialog()
            self.langD.exec()
            self.target=select_lang.mainlang

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
                    btnPlay=QPushButton("▶")
                    btnPlay.setMaximumWidth(250)
                    btnPlay.setMinimumHeight(250)
                    btnPlay.setStyleSheet(
                        '''
                        QPushButton{
                        font: 30pt;
                        border-radius: 20px;
                        background-color: #6a89cc;
                        color: rgb(0,0,0);
                        text-align: bottom;
                        }
                        QPushButton:hover{
                        font: 30pt;
                        border-radius: 20px;
                        background-color: #535c68;
                        color: rgb(255, 255, 255);
                        }
                        QPushButton:pressed{
                        background-color: rgb(255, 255, 255);
                        border-style: inset;
                        color: rgb(0,0,0);
                        }

                        
                        ''')
                    self.plyOut.addWidget(btnPlay)
                    btnPlay.clicked.connect(lambda :self.play())



            elif(i=='STT'):
                stt.stt(self.fileDir)
                print(stt.stt_res)
                if (lw.item(last).text() == 'TTS'):
                    self.outputText.setText(stt.stt_res)
            elif(i=='번역'):
                print(self.text,self.source,self.target)
                text_translation.trans(self.text,self.source,self.target)

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

    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileDir)
        pygame.mixer.music.play()
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


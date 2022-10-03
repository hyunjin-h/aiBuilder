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
import tts, stt,text_translation,select_lang,input_text,OCR,detection,lang_detect,face,model

form_class = uic.loadUiType("_uiFiles/mainPage.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.txt=""
        self.fileDir=''
        self.source=''
        self.target=''


    def initUI(self):
        self.mainList.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        self.runBtn.clicked.connect(self.runModel)
        self.resetBtn.clicked.connect(self.clear)
        self.closeBtn.clicked.connect(self.close)

        self.closeBtn.setStyleSheet('''
                                    QPushButton{
                                    background-color: transparent;
                                    border-image:url("image/close.png");
                                    }
                                    '''
                                    )
        
        self.fileList.setSpacing(8)
        self.inputList.setSpacing(8)
        self.modelList.setSpacing(8)
        self.mainList.setSpacing(10)

        l1 = QListWidgetItem(QIcon('image/text.png'), "text")
        l2 = QListWidgetItem(QIcon('image/image.png'), "image")
        l3 = QListWidgetItem(QIcon('image/sound.png'), "sound")
        self.fileList.insertItem(0, l1)
        self.fileList.insertItem(1,l2)
        self.fileList.insertItem(2,l3)

        i1 = QListWidgetItem(QIcon('image/camera.png'), "camera")
        i2 = QListWidgetItem(QIcon('image/mic.png'), "mic")
        i3 = QListWidgetItem(QIcon('image/draw.png'), "draw")
        self.inputList.insertItem(0, i1)
        self.inputList.insertItem(1, i2)
        self.inputList.insertItem(2, i3)

        m1 = QListWidgetItem(QIcon('image/trans.png'), "번역")
        m2 = QListWidgetItem(QIcon('image/imgtrans.png'), "이미지번역")
        m3 = QListWidgetItem(QIcon('image/tts.png'), "TTS")
        m4 = QListWidgetItem(QIcon('image/stt.png'), "STT")
        m5 = QListWidgetItem(QIcon('image/ocr.png'), "OCR")
        m6 = QListWidgetItem(QIcon('image/obj.png'), "Object Detection")
        m7 = QListWidgetItem(QIcon('image/face.png'), "Face Recognition")
        m8 = QListWidgetItem(QIcon('image/imggen.png'), "Image Generation")
        m9 = QListWidgetItem(QIcon('image/cal.png'), "AI calculator")
        self.modelList.insertItem(0, m1)
        self.modelList.insertItem(1, m2)
        self.modelList.insertItem(2, m3)
        self.modelList.insertItem(3, m4)
        self.modelList.insertItem(4, m5)
        self.modelList.insertItem(5, m6)
        self.modelList.insertItem(6, m7)
        self.modelList.insertItem(7, m8)
        self.modelList.insertItem(8, m9)


    def close(self):
        sys.exit()


    def chkItemDoubleClicked(self):
        rowNum=self.mainList.currentRow()
        rowText=self.mainList.currentItem().text()
        print(str(rowNum) + " : " + rowText)


        if(rowText=='text'):
            self.inputTxt=TextDialog()
            self.inputTxt.exec()
            self.txt=self.inputTxt.text
            lang_detect.detect_lang(self.txt)
            self.source=lang_detect.lang


        elif(rowText=='image'):
            self.fileopen()
        elif(rowText=='sound'):
            self.fileopen()
        elif(rowText=='camera'):

            os.system('python cam.py')
            try:
                self.fileDir='image/input_photo.jpg'
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

        elif(rowText=='draw'):
            os.system('python drawing.py')
            try:
                self.fileDir='image/i.png'
            except:
                pass
        elif(rowText=='image'):
            print(rowText)

    def runModel(self):
        lw = self.mainList
        last=lw.count()-1
        print(last)
        items = [lw.item(x).text() for x in range(lw.count())]
        for i in items:
            if(i=='TTS'):
                tts.tts(self.txt,self.source)
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
                self.txt=stt.stt_res
                self.source='ko' #추후에 직접 입력할 수 있도록 할것임
                if (lw.item(last).text() == 'STT'):
                    self.outputText.setText(stt.stt_res)
            elif(i=='번역'):
                text_translation.trans(self.txt,self.source,self.target)
                self.source=self.target
                trans=text_translation.trans_res
                self.txt=trans
                if (lw.item(last).text() == '번역'):
                    self.outputText.setText(trans)
            elif(i=='이미지번역'):
                print(items[i + 1])
            elif(i=='OCR'):
                OCR.ocr(self.fileDir)
                print(OCR.ocr_res)
                if (lw.item(last).text() == 'OCR'):
                    self.outputText.setText(OCR.ocr_res)
            elif(i=='Object Detection'):
                detection.object_detect(self.fileDir)
                obj_res = ' '.join(s for s in detection.obj_res)
                self.txt=obj_res
                self.source='en'
                if (lw.item(last).text() == 'Object Detection'):
                    self.outputText.setText(self.txt)

            elif(i=='Face Recognition'):

                face.face(self.fileDir)
                face_result=face.face_result
                self.txt=face_result
                if (lw.item(last).text() == 'Face Recognition'):
                    self.outputText.setText(self.txt)
            elif (i == 'AI calculator'):
                try:
                    final = model.test_pipeline_equation(self.fileDir)
                    self.outputText.setText(final)
                except:
                    print("error")
                    self.outputText.setText("해당 수식을 인식할 수 없습니다.")
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
        self.outputText.clear()



    def fileopen(self):
        global filename
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.fileDir = f'{filename[0]}'
        print(self.fileDir)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


import os
import sys
import time

import cv2
import pygame


from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic,QtCore,QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import  RecorD
from input_text import TextDialog
from select_lang import LangDialog
from recordTest import Window
from odOut import odDialog
import tts, stt,text_translation,select_lang,input_text,OCR,detection,lang_detect,face,model,dalle,odOut,plotter,recordTest
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
        dir_s = 'C:/22_IF028/22_if028/soundFiles/'
        if os.path.exists(dir_s):
            for f in os.scandir(dir_s):
                os.remove(f.path)
            print('done')
        else:
            print('no')




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

        QToolTip.setFont(QFont('나눔스퀘어_ac bold', 15))

        l1 = QListWidgetItem(QIcon('image/text.png'), "text")
        l1.setToolTip('<font color=#177e89>텍스트</font><br><font size=2>텍스트 입력</font>')
        l2 = QListWidgetItem(QIcon('image/image.png'), "image")
        l2.setToolTip('<font color=#e76f51>이미지</font><br><font size=2>로컬 이미지 파일</font>')
        l3 = QListWidgetItem(QIcon('image/sound.png'), "sound")
        l3.setToolTip('<font color=#fca311>음성</font><br><font size=2>로컬 음성 파일</font>')

        self.fileList.insertItem(0, l1)
        self.fileList.insertItem(1,l2)
        self.fileList.insertItem(2,l3)

        i1 = QListWidgetItem(QIcon('image/camera.png'), "camera")
        i1.setToolTip('<font color=#e76f51>이미지</font><br><font size=2>웹캠을 이용한 실시간 캡처</font>')
        i2 = QListWidgetItem(QIcon('image/mic.png'), "mic")
        i2.setToolTip('<font color=#fca311>음성</font><br><font size=2>마이크를 이용한 실시간 녹음</font>')
        i3 = QListWidgetItem(QIcon('image/draw.png'), "draw")
        i3.setToolTip('<font color=#e76f51>이미지</font><br><font size=2>손글씨 그림판</font>')
        self.inputList.insertItem(0, i1)
        self.inputList.insertItem(1, i2)
        self.inputList.insertItem(2, i3)

        m1 = QListWidgetItem(QIcon('image/trans.png'), "번역")
        m1.setToolTip('입력: <font color=#177e89>텍스트</font><br>출력: <font color=#177e89>텍스트</font><br><font size=2>텍스트 번역</font>')
        m2 = QListWidgetItem(QIcon('image/imgtrans.png'), "이미지번역")
        m2.setToolTip('입력: <font color=#e76f51>이미지</font><br>출력: <font color=#e76f51>이미지</font><br><font size=2>원본 이미지에 번역 결과를 합성한 이미지 출력</font>')
        m3 = QListWidgetItem(QIcon('image/tts.png'), "TTS")
        m3.setToolTip('입력: <font color=#177e89>텍스트</font><br>출력: <font color=#fca311>음성</font><br><font size=2>텍스트를 음성으로 변환</font>')
        m4 = QListWidgetItem(QIcon('image/stt.png'), "STT")
        m4.setToolTip('입력: <font color=#fca311>음성</font><br>출력: <font color=#177e89>텍스트</font><br><font size=2>음성인식 후 텍스트로 변환</font>')
        m5 = QListWidgetItem(QIcon('image/ocr.png'), "OCR")
        m5.setToolTip('입력: <font color=#e76f51>이미지</font><br>출력: <font color=#177e89>텍스트</font><br><font size=2>이미지 내의 텍스트 추출</font>')
        m6 = QListWidgetItem(QIcon('image/obj.png'), "Object Detection")
        m6.setToolTip('''입력: <font color=#177e89>텍스트</font>, <font color=#e76f51>이미지</font>
        <br>출력: <font color=#177e89>텍스트</font>, <font color=#9381ff>XY 플로터</font>
        <br><font size=2>(1) 찾으려는 대상 텍스트 입력, 기기가 대상을 찾음
        <br>(2) 이미지 인식한 물체들 텍스트 리스트로 출력</font>''')
        m7 = QListWidgetItem(QIcon('image/face.png'), "Face Recognition")
        m7.setToolTip('입력: <font color=#e76f51>이미지</font><br>출력: <font color=#177e89>텍스트</font><br><font size=2>얼굴이미지로 성별, 나이, 기분 예측</font>')
        m8 = QListWidgetItem(QIcon('image/imggen.png'), "Image Generation")
        m8.setToolTip('입력: <font color=#177e89>텍스트</font><br>출력: <font color=#e76f51>이미지</font><br><font size=2>텍스트 기반 이미지 생성</font>')
        m9 = QListWidgetItem(QIcon('image/cal.png'), "AI calculator")
        m9.setToolTip('입력: <font color=#e76f51>이미지</font><br>출력: <font color=#177e89>텍스트</font><br><font size=2>손글씨 수식을 인식하여 수식 및 결과값 출력</font>')
        m10 = QListWidgetItem( "celebrity")
        m11 = QListWidgetItem( "pose estimation")
        m12 = QListWidgetItem("summary")

        self.modelList.insertItem(0, m1)
        self.modelList.insertItem(1, m2)
        self.modelList.insertItem(2, m3)
        self.modelList.insertItem(3, m4)
        self.modelList.insertItem(4, m5)
        self.modelList.insertItem(5, m6)
        self.modelList.insertItem(6, m7)
        self.modelList.insertItem(7, m8)
        self.modelList.insertItem(8, m9)
        self.modelList.insertItem(9,m10)
        self.modelList.insertItem(10, m11)
        self.modelList.insertItem(11, m12)

        # self.btnList=[]
        # self.pltBtn.itemDoubleClicked.connect(self.odBtnClicked)
        # self.pltBtn.setSpacing(20)

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
                print(self.fileDir)
            except:
                pass
        elif(rowText=='mic'):
            # RecorD.main()
            # filepath = RecorD.filename
            # specialChars = "\\"
            # for specialChar in specialChars:
            #     filepath = filepath.replace(specialChar, '/')
            #     print(filepath)
            # self.fileDir=filepath

            os.system('python recordTest.py')
            try:
                self.fileDir='soundFiles/input.wav'
                print(self.fileDir)
            except:
                pass







        elif(rowText=='번역'):
            self.langD = LangDialog()
            self.langD.exec()
            self.target=select_lang.mainlang
            print(self.target)

        elif(rowText=='draw'):
            os.system('python drawing.py')
            try:
                self.fileDir='image/i.png'
            except:
                pass
        elif(rowText=='image'):
            print(rowText)
        elif (rowText == 'Object Detection'):
            self.odo = odDialog()
            self.odo.exec()

    def runModel(self):
        lw = self.mainList
        last=lw.count()-1
        print(last)
        items = [lw.item(x).text() for x in range(lw.count())]
        for i in items:
            if(i=='TTS'):
                tts.tts(self.txt,self.source)
                self.fileDir=tts.sound_path
                if(lw.item(last).text()=='TTS'):
                    btnPlay=QPushButton("▶")
                    btnPlay.setMaximumWidth(300)
                    btnPlay.setMinimumHeight(300)
                    btnPlay.setStyleSheet(
                        '''
                        QPushButton{
                        font: 30pt;
                        border-radius: 20px;
                        background-color: #6a89cc;
                        color: rgb(255,255,255);
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
                    btnPlay.clicked.connect(self.play)

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
                self.txt=OCR.ocr_res
                lang_detect.detect_lang(self.txt)
                self.source = lang_detect.lang
                if (lw.item(last).text() == 'OCR'):
                    self.outputText.setText(self.txt)
            elif(i=='Object Detection'):
                if (odOut.odod == 0):
                    detection.object_detect(self.fileDir)
                    obj_res_txt = ' '.join(s for s in detection.obj_res_name)
                    self.txt = obj_res_txt
                    self.source = 'en'
                if (odOut.odod == 1):
                    # 카메라 촬영
                    cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)  # 노트북 웹캠을 카메라로 사용 #걍 카메라는 여기 1번으로 고치기
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    start = time.time()
                    while cv2.waitKey(33) < 0:
                        ret, frame = cap.read()
                        # cv2.imshow("VideoFrame", frame)
                        end = time.time()
                        if (end-start)>3:
                            file = 'image/plotter.jpeg'
                            cv2.imwrite(file, frame)
                            print(file, ' saved')
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                    self.fileDir='image/plotter.jpeg'
                    detection.object_detect(self.fileDir)


                if (lw.item(last).text() == 'Object Detection'):
                    if(odOut.odod==0):
                        self.outputText.setText(self.txt)
                    if (odOut.odod == 1):
                        plotter.Plotter(self.txt)

            elif(i=='Face Recognition'):
                face.face(self.fileDir)
                face_result=face.face_result
                self.txt=face_result
                self.source = 'ko'
                if (lw.item(last).text() == 'Face Recognition'):
                    self.outputText.setText(self.txt)

            elif (i == 'Image Generation'):
                try:
                    dalle.dalle(self.txt)

                    img = cv2.imread('image/dalle.png')
                    # --② 배율 지정으로 확대
                    dst2 = cv2.resize(img, None, None, 2, 2, cv2.INTER_CUBIC)
                    cv2.imwrite('image/dalleBig.png', dst2)
                    self.fileDir = 'image/dalleBig.png'
                    dallePixmap=QPixmap(self.fileDir)
                    self.outputImage.setPixmap(dallePixmap)

                    print('image')
                except:
                    print("error")
                    self.outputText.setText("해당 수식을 인식할 수 없습니다.")



            elif (i == 'AI calculator'):
                try:
                    final = model.test_pipeline_equation(self.fileDir)
                    self.outputText.setText(final)
                except:
                    print("error")
                    self.outputText.setText("해당 수식을 인식할 수 없습니다.")


            else:
                pass
    # def createBtn(self):
    #     for i in range(detection.obj_cnt):
    #         self.btnList.append(QListWidgetItem(detection.obj_res_name[i]))
    #         self.pltBtn.insertItem(i, self.btnList[i])
    # def odBtnClicked(self):
    #     od_rowNum = self.pltBtn.currentRow()
    #     od_rowText = self.pltBtn.currentItem().text()
    #     print(str(od_rowNum) + " : " + od_rowText)
    #     if(od_rowNum>=0):
    #         plotter.Plotter(od_rowNum)
    def timego(self):
        time.sleep(2)
    def play(self):
        print(self.fileDir)
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileDir)
        pygame.mixer.music.play()
    def clear(self):
        self.txt = ''
        self.fileDir = ''
        self.source=''
        self.target=''
        self.mainList.clear()
        self.outputText.clear()
        self.outputImage.clear()
        for i in reversed(range(self.plyOut.count())):
            self.plyOut.itemAt(i).widget().setParent(None)
        dir_s = 'C:/22_IF028/22_if028/soundFiles/'
        if os.path.exists(dir_s):
            for f in os.scandir(dir_s):
                try:
                    os.remove(f.path)
                except:
                    pass
            print('done')
        else:
            print('no')




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


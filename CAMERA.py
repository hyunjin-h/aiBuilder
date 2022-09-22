import sys
import threading
import cv2
from PyQt5 import QtGui
from PyQt5 import QtWidgets


running=False

def run():
    global running
    cap=cv2.VideoCapture(0)
    width=cap.set(cv2.CAP_PROP_FRAME_WIDTH,600)
    height=cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
    label.resize(round(width),round(height))



    while running:
        ret, img = cap.read()
        if ret:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            h,w,c=img.shape
            qImg=QtGui.QImage(img.data,w,h,w*c,QtGui.QImage.Format_RGB888)
            pixmap=QtGui.QPixmap.fromImage(qImg)
            label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(win,"Error","Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Thread end.")



def save():
    global running
    running=True
    th=threading.Thread(target=run)
    th.start()
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    file = 'input_photo.jpg'
    cv2.imwrite(file, img)
    print(file, ' saved')

def stop():
    global running
    running = False
    print("quit..")
    quit()

app=QtWidgets.QApplication([])
win=QtWidgets.QWidget()
vbox=QtWidgets.QVBoxLayout()
label=QtWidgets.QLabel()

btn_save=QtWidgets.QPushButton("SAVE")
btn_quit=QtWidgets.QPushButton("Quit")

vbox.addWidget(label)
vbox.addWidget(btn_save)
vbox.addWidget(btn_quit)
win.setLayout(vbox)
win.show()

btn_save.clicked.connect(save)
btn_quit.clicked.connect(stop)

sys.exit(app.exec_())
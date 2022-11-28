import sys
import wave
import os,tempfile

import pyaudio as pa
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class RecordingThread(QThread):

    stopped = False
    sig_started = pyqtSignal()
    sig_stopped = pyqtSignal()

    def __init__(self, target_file):
        self.target_file = target_file
        super().__init__()

    def run(self) -> None:
        audio = pa.PyAudio()
        frames = []
        stream = audio.open(format=pa.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.stopped = False
        self.sig_started.emit()

        while not self.stopped:
            data = stream.read(1024)
            frames.append(data)

        stream.close()

        self.sig_stopped.emit()

        wf = wave.open(self.target_file, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pa.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

    @pyqtSlot()
    def stop(self):
        self.stopped = True


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("audio")
        self.resize(500, 500)
        self.setStyleSheet("background-color: #ecf0f1;	"
                           )

        self.setMinimumSize(QSize(500,500))
        self.setMaximumSize(QSize(500,500))

        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create recording thread and attach slots to its signals
        # self.filename = tempfile.mktemp(
        #     prefix='hanium_', suffix='.wav', dir='soundFiles')
        self.recording_thread = RecordingThread(target_file='soundFiles/input.wav')
        self.recording_thread.sig_started.connect(self.recording_started)
        self.recording_thread.sig_stopped.connect(self.recording_stopped)

        self.centralwidget = QWidget(self)
        self.eLabel = QLabel(self.centralwidget)
        self.eLabel.setGeometry(QRect(0, 0, 500, 500))
        self.eLabel.setStyleSheet("border :10px solid black;border-radius:20px;\n")
        self.labelRec = QLabel(self.centralwidget)

        self.labelRec.setGeometry(QRect(100, 100, 300, 100))
        self.labelRec.setStyleSheet("font: 14pt 'NanumSquare';\n")

        self.recbtn = QPushButton(self.centralwidget)

        self.recbtn.setGeometry(QRect(87, 250, 100, 100))
        self.recbtn.setStyleSheet('''QPushButton{background-color: transparent;
                                    border-image:url("image/record.png");}''')

        # self.recbtn.setText("확인")
        # Connect signal "recbtn.clicked" to the slot "recording_thread.start" of our QThread
        # Never connect directly to the run, always to start!
        self.recbtn.clicked.connect(self.recording_thread.start)

        self.stopbtn = QPushButton(self.centralwidget)


        self.stopbtn.setGeometry(QRect(300, 250, 100, 100))
        self.stopbtn.setStyleSheet('''QPushButton{background-color: transparent;
                                    border-image:url("image/stop.png");}''')
        # self.stopbtn.setText("확인")
        self.stopbtn.setDisabled(True)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QRect(200, 400, 100, 50))
        self.pushButton_3.setStyleSheet("border-radius:20px;\n"
                                        "font: 12pt 'NanumSquare';\n"
                                        "    background-color: #2f3640;\ncolor: #fff;\n"
                                        )
        self.pushButton_3.setText("확인")
        self.pushButton_3.clicked.connect(self.salir)

        # Connect signal "stopbtn.clicked" to the slot "recording_thread.stop" of our QThread
        self.stopbtn.clicked.connect(self.recording_thread.stop)


    @pyqtSlot()
    def recording_started(self):
        """This slot is called when recording starts"""
        self.labelRec.setText('◉ recording...')
        self.stopbtn.setDisabled(False)
        self.recbtn.setDisabled(True)

    @pyqtSlot()
    def recording_stopped(self):
        """This slot is called when recording stops"""
        self.labelRec.setText('recording stopped')
        self.recbtn.setDisabled(False)
        self.stopbtn.setDisabled(True)
    def salir(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec()
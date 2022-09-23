import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = uic.loadUiType("_uiFiles/mainPage.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.mainList.itemDoubleClicked.connect(self.chkItemDoubleClicked)
        self.runBtn.clicked.connect(self.runModel)

    def chkItemDoubleClicked(self):
        rowNum=self.mainList.currentRow()
        rowText=self.mainList.currentItem().text()
        print(str(rowNum) + " : " + rowText)
        if(rowText=='text'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)
        elif(rowText=='mic'):
            print(rowText)
        elif(rowText=='camera'):
            print(rowText)
        elif(rowText=='draw'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)
        elif(rowText=='image'):
            print(rowText)

    def runModel(self):
        rowNum=self.mainList.currentRow()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


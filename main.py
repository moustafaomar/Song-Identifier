from PyQt5 import QtCore, QtGui, QtWidgets
from song import Song
import numpy as np
import logging
logging.basicConfig(filename="logging.log", format='%(asctime)s %(message)s', filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 
class Ui_MainWindow(object):
    def __init__(self):
        self.songs = np.array([Song(None),Song(None)])
        self.mixed = Song(None)
    def mix(self):
        factor = self.horizontalSlider.value()
        logger.debug('Mixer called with slider value %s',factor)
        self.songs[0].mix(self.songs[1],factor)
        self.mixed.loadSong('mix.wav')
        List = self.mixed.getSimilarity()
        List.sort(key=lambda x: x[0],reverse = True)
        self.resultsTable.setRowCount(len(List))
        for row in range(len(List)):
            self.resultsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(List[row][1]))
            self.resultsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(List[row][0], 2))))
    def UI_starter(self):
         self.horizontalSlider.hide()
         self.resultsTable.hide()  
    def loadSong(self,id):
        try:
                song = QtWidgets.QFileDialog.getOpenFileName(None, "Load song %s",filter="*.mp3 *.wav")
                path=song[0]
                logger.debug('Opening file at path %s',path)
                self.songs[id].loadSong(path)
                checkSongs = self.songs[0].path != None and self.songs[1].path != None
                self.resultsTable.show()
                if(checkSongs):
                        self.horizontalSlider.show()
                List = self.songs[id].getSimilarity()
                List.sort(key=lambda x: x[0],reverse = True)
                self.resultsTable.setRowCount(len(List))
                for row in range(len(List)):
                        self.resultsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(List[row][1]))
                        self.resultsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(List[row][0], 2))))
        except:
                logger.debug('No song specified or invalid file')
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 800)
        MainWindow.setStyleSheet("\n"
"background-color: rgb(40, 53, 51);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralwidget.setObjectName("centralwidget")
        self.song1 = QtWidgets.QPushButton(self.centralwidget)
        self.song1.setStyleSheet("background-color: rgb(255, 219, 34);\n"
"color: rgb(0, 0, 0);\n"
"\n"
"")
        self.song1.setObjectName("song1")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setFixedWidth(500)
        self.horizontalSlider.sliderReleased.connect(lambda:self.mix())
        self.song2 = QtWidgets.QPushButton(self.centralwidget)
        self.song2.setStyleSheet("background-color: rgb(255, 219, 34);\n"
"color: rgb(0, 0, 0);\n"
"\n"
"")
        self.song2.setObjectName("song2")
        self.song1.clicked.connect(lambda:self.loadSong(0))
        self.song2.clicked.connect(lambda:self.loadSong(1))
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.textBrowser_3.setObjectName("textBrowser_3")
        textGB = QtWidgets.QGroupBox()
        text  = QtWidgets.QHBoxLayout(self.centralwidget)
        text.addWidget(self.textBrowser_2)
        text.addWidget(self.textBrowser_3)
        textGB.setLayout(text)
        textGB.setFixedHeight(100)
        self.layout.addWidget(textGB)
        buttonsGB = QtWidgets.QGroupBox()
        self.song1.setFixedHeight(50)
        self.song2.setFixedHeight(50)
        buttons = QtWidgets.QHBoxLayout(self.centralwidget)
        buttons.addWidget(self.song1)
        buttons.addWidget(self.song2)
        buttonsGB.setLayout(buttons)
        self.layout.addWidget(buttonsGB)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 458, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.resultsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.resultsTable.setObjectName("resultsTable")
        self.resultsTable.setColumnCount(2)
        self.resultsTable.setFixedWidth(300)
        self.layout.addWidget(self.horizontalSlider,alignment=QtCore.Qt.AlignHCenter)
        self.UI_starter()
        self.layout.addWidget(self.resultsTable,alignment=QtCore.Qt.AlignHCenter)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.song1.setText(_translate("MainWindow", "New song"))
        self.song2.setText(_translate("MainWindow", "New song"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Song 1</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p></body></html>"))
        self.textBrowser_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Song 2</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

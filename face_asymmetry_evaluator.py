# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'face_asymmetryPCELKB.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(597, 228)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QRect(30, 60, 111, 23))
        self.pushButton.setCheckable(False)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QRect(30, 100, 111, 23))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setGeometry(QRect(30, 140, 121, 23))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(30, 20, 111, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 20, 341, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(160, 60, 151, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(160, 100, 191, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(160, 140, 271, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Face Asymmetry Evaluator", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Take Face Pictures", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Create Point Cloud", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Evaluate Asymmetry", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Camera Calibration", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"If the camera already calibrated, you do not have to calibrate again.", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Take face images using camera", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Create point cloud using image folder.", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Evaluate asymmetry using point cloud and pictures.", None))
    # retranslateUi
    
def calibration_exec(filename):
	print("here")
	cwd = os.getcwd()
	os.chdir('./calibration')
	os.system('sudo python3 calibration.py')
	os.chdir(cwd)

def image_save(location):
	cwd = os.getcwd()
	os.chdir('./sfm')
	os.system('sudo python3 imgsave.py')
	os.chdir(cwd)
def sfm_run(files):
	cwd = os.getcwd()
	os.chdir('./sfm')
	os.system('python3 SfM_SequentialPipeline.py images results')
	os.chdir(cwd)
def evaluate_asymmetry(asymmetry):
	cwd = os.getcwd()
	os.chdir('./dlib')
	os.system('python3 dlib_facial.py')
	os.chdir(cwd)
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	ex = Ui_MainWindow()
	w = QMainWindow()
	ex.setupUi(w)
	w.show()
	filename = 'test'
	location = 'location'
	files = 'files'
	asymmetry = 'asymmetry'
	
	ex.pushButton_4.clicked.connect(lambda: calibration_exec(filename))
	ex.pushButton.clicked.connect(lambda: image_save(location))
	ex.pushButton_2.clicked.connect(lambda: sfm_run(files))
	ex.pushButton_3.clicked.connect(lambda: evaluate_asymmetry(asymmetry))
	sys.exit(app.exec_())


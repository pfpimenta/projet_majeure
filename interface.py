# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projetMajeure.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(845, 583)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.playpause = QtWidgets.QPushButton(self.centralwidget)
		self.playpause.clicked.connect(MainWindow.game.playPause) # ajoutee
		self.playpause.setGeometry(QtCore.QRect(530, 30, 141, 27))
		self.playpause.setObjectName("playpause")
		self.reset = QtWidgets.QPushButton(self.centralwidget)
		self.reset.clicked.connect(MainWindow.game.reset) # ajoutee
		self.reset.setGeometry(QtCore.QRect(700, 30, 131, 27))
		self.reset.setObjectName("reset")
		self.gameWidget = gameWidget(self.centralwidget, MainWindow.game)
		self.gameWidget.setGeometry(QtCore.QRect(20, 20, 500, 500))
		self.gameWidget.setObjectName("gameWidget")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(530, 70, 131, 17))
		self.label.setObjectName("label")
		self.e1 = QtWidgets.QLabel(self.centralwidget)
		self.e1.setGeometry(QtCore.QRect(530, 110, 71, 17))
		self.e1.setObjectName("e1")
		self.learningRate = QtWidgets.QLabel(self.centralwidget)
		self.learningRate.setGeometry(QtCore.QRect(530, 210, 111, 17))
		self.learningRate.setObjectName("learningRate")
		self.e2 = QtWidgets.QLabel(self.centralwidget)
		self.e2.setGeometry(QtCore.QRect(710, 110, 61, 17))
		self.e2.setObjectName("e2")
		self.rSpawnRate = QtWidgets.QLabel(self.centralwidget)
		self.rSpawnRate.setGeometry(QtCore.QRect(530, 170, 151, 17))
		self.rSpawnRate.setObjectName("rSpawnRate")
		self.rdmPathProb = QtWidgets.QLabel(self.centralwidget)
		self.rdmPathProb.setGeometry(QtCore.QRect(530, 250, 151, 17))
		self.rdmPathProb.setObjectName("rdmPathProb")
		self.timePeriod = QtWidgets.QLabel(self.centralwidget)
		self.timePeriod.setGeometry(QtCore.QRect(530, 330, 151, 17))
		self.timePeriod.setObjectName("timePeriod")
		self.timeModulo = QtWidgets.QLabel(self.centralwidget)
		self.timeModulo.setGeometry(QtCore.QRect(530, 360, 151, 17))
		self.timeModulo.setObjectName("timeModulo")
		self.nbEpisodesLabel = QtWidgets.QLabel(self.centralwidget)
		self.nbEpisodesLabel.setGeometry(QtCore.QRect(530, 470, 151, 17))
		self.nbEpisodesLabel.setObjectName("nbEpisodesLabel")
		self.spinBoxE1 = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxE1.setGeometry(QtCore.QRect(600, 100, 51, 27))
		self.spinBoxE1.setObjectName("spinBoxE1")
		self.spinBoxE2 = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxE2.setGeometry(QtCore.QRect(780, 100, 51, 27))
		self.spinBoxE2.setObjectName("spinBoxE2")
		self.nbEpisodes = QtWidgets.QLabel(self.centralwidget)
		self.nbEpisodes.setGeometry(QtCore.QRect(680, 460, 51, 31))
		self.nbEpisodes.setObjectName("nbEpisodes")
		self.SpinBoxLearningRate = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.SpinBoxLearningRate.setGeometry(QtCore.QRect(690, 200, 141, 27))
		self.SpinBoxLearningRate.setDecimals(10)
		self.SpinBoxLearningRate.setObjectName("SpinBoxLearningRate")
		self.SpinBoxTimePeriod = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.SpinBoxTimePeriod.setGeometry(QtCore.QRect(650, 320, 91, 27))
		self.SpinBoxTimePeriod.setDecimals(4)
		self.SpinBoxTimePeriod.setObjectName("SpinBoxTimePeriod")
		self.spinBoxModulo = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxModulo.setGeometry(QtCore.QRect(650, 360, 60, 27))
		self.spinBoxModulo.setObjectName("spinBoxModulo")
		self.SpinBoxRSR = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.SpinBoxRSR.setGeometry(QtCore.QRect(690, 160, 141, 27))
		self.SpinBoxRSR.setDecimals(10)
		self.SpinBoxRSR.setObjectName("SpinBoxRSR")
		self.SpinBoxRPP = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.SpinBoxRPP.setGeometry(QtCore.QRect(690, 240, 141, 27))
		self.SpinBoxRPP.setDecimals(10)
		self.SpinBoxRPP.setObjectName("SpinBoxRPP")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 25))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.playpause.setText(_translate("MainWindow", "Play / Pause"))
		self.reset.setText(_translate("MainWindow", "Reset"))
		self.label.setText(_translate("MainWindow", "Nombre d\'Agents"))
		self.e1.setText(_translate("MainWindow", "Equipe 1:"))
		self.learningRate.setText(_translate("MainWindow", "Learning rate : "))
		self.e2.setText(_translate("MainWindow", "Equipe 2:"))
		self.rSpawnRate.setText(_translate("MainWindow", "Resource spawn rate : "))
		self.rdmPathProb.setText(_translate("MainWindow", "Random path prob:"))
		self.timePeriod.setText(_translate("MainWindow", "Time period:"))
		self.timeModulo.setText(_translate("MainWindow", "Time modulo:"))
		self.nbEpisodesLabel.setText(_translate("MainWindow", "Nombre d\'Episodes:"))
		self.nbEpisodes.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">0</span></p></body></html>"))





class gameWidget(QWidget):
	#classe de l'aire d'affichage
	qp = None # Q painter
	brush = None # Q brush
	background_pm = None # pixmap pour le background
	game = None

	def __init__(self, parent, game):
		super().__init__(parent)

		self.qp = QPainter()
		self.game = game

		self.background_pm = QPixmap()
		self.brush = QBrush(Qt.SolidPattern)
	
		self.setGeometry(0, 0, 100, 100)
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.move(300, 300)
		self.show()

	def paintEvent(self, event):
		self.qp.begin(self)
		self.qp.setBrush(self.brush)
		#afficher le background
		self.qp.drawRect(0, 0, 10000, 10000)
		#afficher les objets
		for objet in self.game.objectsList:
			objet.draw(qp)
		# ___
		self.qp.end()


class Fenetre(QtWidgets.QMainWindow):
	#classe d'affichage
	game = None
	def __init__(self, game):
		super().__init__()

		self.game = game
	
		self.setGeometry(300, 300, 350, 100)
		self.setWindowTitle('REINFORCEMENT LEARNING')
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.move(300, 300)
		self.show()




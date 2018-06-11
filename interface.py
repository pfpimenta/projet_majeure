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

# ATTENTION : Ces variables sont également définies dans projetMajeure.py.
# Pensez à les modifier là-bas aussi ou à faire une variable partagée
GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 500

# valeurs initialles de l'interface
INIT_NB_E1 = 1
INIT_NB_E2 = 1
INIT_LEARNING_RATE = 0.1
INIT_RESOURCE_SPAWNING_RATE = 0.02
INIT_RANDOM_PATH_PROB = 0.1
INIT_TIME_PERIOD = 100 # miliseconds entre frames
INIT_TIME_MODULO = 1 

IMAGEPATH_BACKGROUND = "Images/background.jpg"

class Ui_MainWindow(object):
	# classe cree par QtDesigner
	MainWindow = None # ajoutee
	def setupUi(self, MainWindow):
		self.MainWindow = MainWindow
		self.MainWindow.setObjectName("MainWindow")
		self.MainWindow.resize(845, 583)
		self.centralwidget = QtWidgets.QWidget(self.MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.playpause = QtWidgets.QPushButton(self.centralwidget)
		self.playpause.clicked.connect(self.MainWindow.game.playPause) # ajoutee
		self.playpause.setGeometry(QtCore.QRect(530, 30, 141, 27))
		self.playpause.setObjectName("playpause")
		self.reset = QtWidgets.QPushButton(self.centralwidget)
		self.reset.clicked.connect(self.MainWindow.game.reset) # ajoutee
		self.reset.setGeometry(QtCore.QRect(700, 30, 131, 27))
		self.reset.setObjectName("reset")
		self.gameWidget = gameWidget(self.centralwidget, self.MainWindow.game)
		self.gameWidget.setGeometry(QtCore.QRect(20, 20, 500, 500))
		self.gameWidget.setObjectName("gameWidget")
		self.nbAgents = QtWidgets.QLabel(self.centralwidget)
		self.nbAgents.setGeometry(QtCore.QRect(530, 70, 131, 17))
		self.nbAgents.setObjectName("nbAgents")
		self.e1 = QtWidgets.QLabel(self.centralwidget)
		self.e1.setGeometry(QtCore.QRect(530, 110, 71, 17))
		self.e1.setObjectName("e1")
		self.e2 = QtWidgets.QLabel(self.centralwidget)
		self.e2.setGeometry(QtCore.QRect(710, 110, 61, 17))
		self.e2.setObjectName("e2")
		self.timePeriod = QtWidgets.QLabel(self.centralwidget)
		self.timePeriod.setGeometry(QtCore.QRect(530, 330, 151, 17))
		self.timePeriod.setObjectName("timePeriod")
		self.timeModulo = QtWidgets.QLabel(self.centralwidget)
		self.timeModulo.setGeometry(QtCore.QRect(530, 360, 151, 17))
		self.timeModulo.setObjectName("timeModulo")
		self.spinBoxE1 = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxE1.valueChanged.connect(self.updateNbE1) # ajoutee
		self.spinBoxE1.setGeometry(QtCore.QRect(600, 100, 51, 27))
		self.spinBoxE1.setObjectName("spinBoxE1")
		self.spinBoxE1.setValue(INIT_NB_E1) #ajoutee
		self.spinBoxE2 = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxE2.valueChanged.connect(self.updateNbE2) # ajoutee
		self.spinBoxE2.setGeometry(QtCore.QRect(780, 100, 51, 27))
		self.spinBoxE2.setObjectName("spinBoxE2")
		self.spinBoxE2.setValue(INIT_NB_E2) #ajoutee
		self.SpinBoxTimePeriod = QtWidgets.QDoubleSpinBox(self.centralwidget)
		self.SpinBoxTimePeriod.valueChanged.connect(self.updateTimePeriod) # ajoutee
		self.SpinBoxTimePeriod.setGeometry(QtCore.QRect(650, 320, 91, 27))
		self.SpinBoxTimePeriod.setDecimals(4)
		self.SpinBoxTimePeriod.setObjectName("SpinBoxTimePeriod")
		self.SpinBoxTimePeriod.setRange(1,99999) #ajoutee
		self.SpinBoxTimePeriod.setValue(INIT_TIME_PERIOD) #ajoutee
		self.spinBoxModulo = QtWidgets.QSpinBox(self.centralwidget)
		self.spinBoxModulo.valueChanged.connect(self.updateTimeModulo) # ajoutee
		self.spinBoxModulo.setGeometry(QtCore.QRect(650, 360, 100, 27))
		self.spinBoxModulo.setObjectName("spinBoxModulo")
		self.spinBoxModulo.setRange(1,99999) #ajoutee
		self.spinBoxModulo.setValue(INIT_TIME_MODULO) #ajoutee
		self.MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self.MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 25))
		self.menubar.setObjectName("menubar")
		self.MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
		self.statusbar.setObjectName("statusbar")
		self.MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

	def retranslateUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.playpause.setText(_translate("MainWindow", "Play / Pause"))
		self.reset.setText(_translate("MainWindow", "Reset"))
		self.nbAgents.setText(_translate("MainWindow", "Nombre d\'Agents"))
		self.e1.setText(_translate("MainWindow", "Equipe 1:"))
		self.e2.setText(_translate("MainWindow", "Equipe 2:"))
		self.timePeriod.setText(_translate("MainWindow", "Time period:"))
		self.timeModulo.setText(_translate("MainWindow", "Time modulo:"))

	def updateNbE1(self): # fonction pour le spinbox
		self.MainWindow.game.window_nb_agents_E1 = self.spinBoxE1.value()
	def updateNbE2(self): # fonction pour le spinbox
		self.MainWindow.game.window_nb_agents_E2 = self.spinBoxE2.value()
	def updateTimePeriod(self): # fonction pour le spinbox 
		self.MainWindow.game.window_time_period = self.SpinBoxTimePeriod.value()
	def updateTimeModulo(self): # fonction pour le spinbox 
		self.MainWindow.game.window_time_modulo = self.spinBoxModulo.value()



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
		self.background_pm.load(IMAGEPATH_BACKGROUND)
		#self.background_pm = QPixmap()
		#self.brush = QBrush(Qt.SolidPattern)
	
		self.setGeometry(0, 0, 100, 100)
		#self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.resize(GAME_AREA_WIDTH, GAME_AREA_HEIGHT)
		self.move(300, 300)
		self.show()

	def paintEvent(self, event):
		self.qp.begin(self)
		#self.qp.setBrush(self.brush)
		#afficher le background
		#self.qp.drawRect(0, 0, 10000, 10000)
		self.qp.drawPixmap(0,0, GAME_AREA_WIDTH, GAME_AREA_HEIGHT,self.background_pm)
		#afficher les objets
		for objet in self.game.objectsList:
			objet.draw(self.qp)
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




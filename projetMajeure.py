#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# PROJET MAJEURE - Reinforcement Learning
# ERBACHER, Pierre
# FOLETTO PIMENTA, Pedro
# TIZON, Nicolas

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
PV_INITIAL = 3
DAMAGE = 1
RESOURCE_VALUE = 50
#team = 0 => ressource et block
#team = 1 => agent et tir (équipe bleu)
#team = 2 => agent et tir (équipe rouge)


class Objet:
# classe pour tout les object qui sont dans l'environnement
	x = 0 # valeur par default
	y = 0
	dx = 0 # vitesses
	dy = 0
	box_x = 5 #collision boxes ( largeur et longeur de l'objet)
	box_y = 5
	team = 0
	def __init__(self,x=0,y=0, dx=0, dy=0 ,team = 0):
		self.x = x;
		self.y = y;
		self.dx = dx;
		self.dy = dy;
		self.team = team;
	def move(self):
	# bouger l'agent d'accord avec sa vitesse
		self.x = self.x + self.dx;
		self.y = self.y + self.dy;
	
	def collision(self,obj ):# how to pass object ?
	#verifie la collision entre les objets
		ret = False
		if (self.x + self.box_x < obj.x - obj.box_x and self.x - self.box_x > obj.x + obj.box_x and self.y + self.box_y < obj.y - obj.box_y and self.y - self.box_y > obj.y + obj.box_y):
    			ret = False
		else:
			ret = True
		return ret
			
	def draw(self, painter):
		#affichage de l'objet
		pass #TODO
		

		
class Agent(Objet):
# classe pour les agents
	def __init__(self,x=0,y=0, dx=0, dy=0,team = 0):
		Objet.__init__(self,x,y,dx,dy,team);
		self.pv = PV_INITIAL

	def shoot(self):
		pass  #TODO
		
	def action(self, state):
	# prendre une action
		pass # TODO

	def place_block(self):
	# placer un bloque en face du agent
		pass # TODO
	
class Tir:
# classe pour les tirs
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y,dx,dy,team);
		self.dmg = DAMAGE
		
class Block:
# classe pour les blocks Mur
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y);
		
class Resource:
# classe pour les rescources
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y);
		self.value =  RESOURCE_VALUE


class Area(QWidget):
	#classe d'affichage
	game = None
	qp = None # Q painter
	brush = None # Q brush
	background_pm = None # pixmap pour le background
	def __init__(self, game):
		super().__init__()

		self.qp = QPainter()
		self.game = game
		playPauseButton = QPushButton('Play/Pause', self)
		playPauseButton.clicked.connect(game.playPause)
		playPauseButton.resize(playPauseButton.sizeHint())
		playPauseButton.move(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.1)     

		resetButton = QPushButton('Reset', self)
		resetButton.clicked.connect(game.reset)
		resetButton.resize(resetButton.sizeHint())
		resetButton.move(WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.2) 

		self.background_pm = QPixmap()
		self.brush = QBrush(Qt.SolidPattern)

	
		self.setGeometry(300, 300, 350, 100)
		self.setWindowTitle('REINFORCEMENT LEARNING')
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.move(300, 300)
		self.show()

	def draw(self):
		self.qp.begin(self)
		self.qp.setBrush(self.brush)
		#afficher le background
		self.qp.drawRect(130, 15, 90, 60)
		#afficher les objets
		for objet in self.game.objectsList:
			objet.draw(qp)
		# ___
		self.qp.end()



class Game():
	#class pour gerer le jeu
	objectsList = []
	def __init__(self):
		pass #TODO
	def playPause(self):
		print ("DEBUG play pause")
		pass #TODO
	def reset(self):
		print ("DEBUG reset")
		pass #TODO
	def update(self):
	# appellee a chaque frame
	# mouvement des agents et tires
		for objet in self.objectsList:
			objet.move()
	# collision
		pass #TODO







		
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	game = Game()
	area = Area(game)
	    
	def timeout():
		print("DEBUG timeout")
		game.update()
		area.draw()

	timer = QTimer()
	timer.timeout.connect(timeout)
	timer.start(100)

	sys.exit(app.exec_())

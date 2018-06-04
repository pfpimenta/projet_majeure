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
import numpy as np
import math
PV_INITIAL = 3
DAMAGE = 1
RESOURCE_VALUE = 50
VITESSE = 10
#team = 0 => ressource et block
#team = 1 => agent et tir (équipe bleu)
#team = 2 => agent et tir (équipe rouge)

#Action possible
STOP = 0
MOVE = 1
TRIGO = 2
HORAIRE = 3
SHOOT = 4
BUILD = 5

ACTION = [STOP,MOVE,TRIGO,HORAIRE,SHOOT,BUILD]


H = 256
W = 256

class Objet:
# classe pour tout les object qui sont dans l'environnement
	x = 0 # valeur par default
	y = 0
	dx = 0 # vitesses
	dy = 0
	angle = 0
	box_x = 5 #collision boxes ( largeur et longeur de l'objet)
	box_y = 5
	team = 0
	type_obj = 0

	def __init__(self,x=0,y=0, dx=0, dy=0 ,angle = 0, team = 0,type_obj = 0):
		self.x = x;
		self.y = y;
		self.dx = dx;
		self.dy = dy;
		self.angle = angle
		self.team = team;
	
	def move(self):
	# bouger l'agent et tir d'accord avec sa vitesse
		self.x = max(0,self.x + self.dx)
		self.y = max(0,self.y + self.dy)
	
	def collision(self,obj ):
	#verifie la collision entre les objets
		ret = False
		if (self.x + self.box_x < obj.x - obj.box_x and self.x - self.box_x > obj.x + obj.box_x and self.y + self.box_y < obj.y - obj.box_y and self.y - self.box_y > obj.y + obj.box_y):
    			ret = False
		else:
			ret = True
		return ret
			
	def draw(self):
		#affichage de l'objet
		pass #TODO
		

		
class Agent(Objet):
# classe pour les agents
	current_action = 0
	def __init__(self,x=0,y=0, dx=0, dy=0,team = 0):
		Objet.__init__(self,x,y,dx,dy,team);
		self.pv = PV_INITIAL

	def shoot(self):
		Tir(agent)
		
	def action(self, state):
	# prendre une action
		
		if (current_action == STOP):
			pass
		
		if (current_action == MOVE):
			self.dy =  int(round(VITESSE*sin(agent.angle))) #maj des prochains dépacment
			self.dx = int(round(VITESSE*cos(agent.angle)))

		if (current_action == TRIGO):
			self.angle = angle + dr
		if (current_action == HORAIRE)
			self.angle = angle - dr
		
		if(current_action == SHOOT):
			shoot()

	def distance(self,objet):
		return np.sqrt((objet.x - self.x)*(objet.x - self.x) + (objet.y - self.y)*(objet.y - self.y))

	def angle(self,objet):
		return math.atan2(objet.y - agent.y , objet.x - agent.x)

	def place_block(self):
	# placer un bloque en face du agent
		pass # TODO
	
class Tir(Objet):
# classe pour les tirs

	def __init__(self,agent):
		self.dy =  int(round(VITESSE*sin(agent.angle))) #maj des prochains dépacment
		self.dx = int(round(VITESSE*cos(agent.angle)))
		Objet.__init__(self,agent.x,agent.y,dx,dy,agent.team,agent.angle);
		self.dmg = DAMAGE


		
class Block(Objet):
# classe pour les blocks Mur
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y);
		
class Resource(Objet):
# classe pour les rescources
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y);
		self.value =  RESOURCE_VALUE






grid_area = np.zeros(H,W)
for i in range(len(objets)):
	grid_area[objets.x][objets.y] = objet.type





class State():

	def_ini_(self,agent,objets):
		for i in objets:
			if (i.type == 1:) #AGENT DE LA MEME EQUIPE
				if (i.team == agent.team):
					self.table_angle_ally.append(agent.angle(i))
					self.table_dist_ally.append(agent.distance(i))
				else:
					self.table_angle_ennemy.append(agent.angle(i))
					self.table_dist_ennemy.append(agent.distance(i))

			if (i.type == 2:) #TIR
				self.table_angle_tir.append(agent.angle(i))
				self.table_dist_tir.append(agent.distance(i))

			if (i.type == 0:) #RESOURCE
				self.table_angle_tir.append(agent.angle(i))
				self.table_dist_tir.append(agent.distance(i))
"""
			if (i.type == 3)#BLOCK
				table_angle_tir.append(agent.angle(i))
				table_dist_tir.append(agent.distance(i))

"""
		
		self.disance_nearest_ennemy = min(self.table_dist_ennemy)
		self.angle_nearest_ennemy = self.table_angle_ennemy(self.table_dist_ennemy.index(self.disance_nearest_ennemy))



		






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
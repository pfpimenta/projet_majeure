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
from interface import *
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
import numpy as np
import math
PV_INITIAL = 3
DAMAGE = 1
RESOURCE_VALUE = 50
VITESSE = 10

#type_obj = 0 => block (pas utilisé actuellement)
#type_obj = 1 => agent
#type_obj = 2 => projectile

#team = 0 => ressource et block
#team = 1 => agent et tir (equipe bleu)
#team = 2 => agent et tir (equipe rouge)

IMAGEPATH_404 = "Images/ImageNotFound.png"
IMAGEPATH_AGENT_BLEU = "Images/AgentBleu.png"
IMAGEPATH_AGENT_ROUGE = "Images/AgentRouge.png"
IMAGEPATH_AGENT_NEUTRE = "Images/AgentNeutre.png"

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
	#team = 0
	#type_obj = 0
	pixmap = None

	def __init__(self,x=0,y=0, dx=0, dy=0 ,angle = 0, team = 0,type_obj = 0):
		self.x = x;
		self.y = y;
		self.dx = dx;
		self.dy = dy;
		self.angle = angle
		self.team = team;
		self.type_obj = type_obj
		pixmapPath = IMAGEPATH_404

		print(team)
		print(type_obj)

		if type_obj == 0:
			#L'objet est un bloc OU on a oublié de mettre type_obj.
			#On s'occupe pas actuellement des blocs.
			pass
		elif type_obj == 1:
			#L'objet est un agent
			if team == 1:
				#Agent bleu
				pixmapPath = IMAGEPATH_AGENT_BLEU
			elif team == 2:
				#Agent rouge
				pixmapPath = IMAGEPATH_AGENT_ROUGE
			else:
				#Agent neutre
				pixmapPath = IMAGEPATH_AGENT_NEUTRE

		elif type_obj == 2:
			#l'objet est un projectile
			pass

		self.pixmap = QPixmap()
		self.pixmap.load(pixmapPath)
			
	
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
			
	def draw(self, qp):
		#affichage de l'objet
		qp.drawPixmap(self.x,self.y, 64, 64, self.pixmap); #peut-être besoin de W et H
		

		
class Agent(Objet):
# classe pour les agents
	def __init__(self,x=0,y=0, dx=0, dy=0, angle = 0, team = 0, act = 0):
		Objet.__init__(self,x,y,dx,dy, angle, team, 1); #type_obj à 1 pour un agent
		self.pv = PV_INITIAL
		self.current_action = act
		

	def shoot(self):
		Tir(agent)
		
	def action(self):
	# prendre une action
		
		if (self.current_action == STOP):
			pass
		
		if (self.current_action == MOVE):
			self.dy =  int(round(VITESSE*np.sin(self.angle))) #maj des prochains deplacement
			self.dx = int(round(VITESSE*np.cos(self.angle)))

		if (self.current_action == TRIGO):
			self.angle = self.angle + dr
		if (self.current_action == HORAIRE):
			self.angle = self.angle - dr
		
		if(self.current_action == SHOOT):
			self.shoot()

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
		self.dy =  int(round(VITESSE*sin(agent.angle))) #maj des prochains deplacement
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






#grid_area = np.zeros(H,W)
#for i in range(len(objets)):
#	grid_area[objets.x][objets.y] = objet.type





class State():

	def __init__(self,agent,objets):
		for i in objets:
			if (i.type == 1): #AGENT DE LA MEME EQUIPE
				if (i.team == agent.team):
					self.table_angle_ally.append(agent.angle(i))
					self.table_dist_ally.append(agent.distance(i))
				else:
					self.table_angle_ennemy.append(agent.angle(i))
					self.table_dist_ennemy.append(agent.distance(i))
			if (i.type == 2): #TIR
				self.table_angle_tir.append(agent.angle(i))
				self.table_dist_tir.append(agent.distance(i))
			if (i.type == 0): #RESOURCE
				self.table_angle_tir.append(agent.angle(i))
				self.table_dist_tir.append(agent.distance(i))
#			if (i.type == 3):#BLOCK
#				table_angle_tir.append(agent.angle(i))
#				table_dist_tir.append(agent.distance(i))
		self.distance_nearest_ennemy = min(self.table_dist_ennemy)
		self.angle_nearest_ennemy = self.table_angle_ennemy(self.table_dist_ennemy.index(self.distance_nearest_ennemy))

		



class Game():
	#class pour gerer le jeu
	def __init__(self):
		self.objectsList = []
		agent1 = Agent(20,20,0,0, 45, 1, 1)
		agent2 = Agent(320,20,0,0,135, 2, 1)
		self.objectsList.extend([agent1, agent2])
	def playPause(self):
		print ("DEBUG play pause")
		pass #TODO
	def reset(self):
		print ("DEBUG reset")
		pass #TODO
	def update(self):
	# appellee a chaque frame
	# exécution des actions des agents
		for objet in self.objectsList:
			if objet.type_obj == 1:
				objet.action()
	# mouvement des agents et tires
		for objet in self.objectsList:
			objet.move()
	# collision
		pass #TODO







		
# main
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	game = Game()
	fenetre = Fenetre(game)
	ui = Ui_MainWindow() # classe cree par QtDesigner
	ui.setupUi(fenetre)
	    
	def timeout():
		# "loop" du jeu
		# print("DEBUG timeout") #debug
		game.update()
		#fenetre.update()
		ui.gameWidget.update()

	timer = QTimer()
	timer.timeout.connect(timeout)
	timer.start(100)
	
	sys.exit(app.exec_())
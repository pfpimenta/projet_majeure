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
import random as rd
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
dr = np.pi/30

#TYPE
AGENT = 1
TIR = 2
RESOURCE = 0

ACTION = [STOP,MOVE,TRIGO,HORAIRE,SHOOT,BUILD]
#TRAINING
N_EPISODE = 100
N_STEP = 10

H = 256
W = 256

#N_STATE = len([0:np.sqrt(H*H+W*W)])
q_table = dict()
eps = 0.1


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
		if (current_action == HORAIRE):
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
				self.table_angle_resource.append(agent.angle(i))
				self.table_dist_resource.append(agent.distance(i))
		#STATE DEFINITION:
		#position ennemi le plus proche
		self.disance_nearest_ennemy = np.min(self.table_dist_ennemy)
		self.angle_nearest_ennemy = self.table_angle_ennemy(self.table_dist_ennemy.index(self.disance_nearest_ennemy))
		#position moyenne allié
		self.mean_disante_ally = np.mean(self.table_dist_ennemy)
		self.mean_angle_ally = np.mean(self.table_angle_ennemy)
		#position ressource la plus proche
		self.distance_nearest_resource = np.min(self.table_dist_resource)
		self.angle_nearest_resource = self.table_angle_resource(self.table_dist_resource.index(self.distance_nearest_resource))
		#position tir le plus proche
		self.disance_nearest_tir = np.min(self.table_dist_tir)
		self.angle_nearest_tir = self.table_angle_tir(self.table_dist_tir.index(self.disance_nearest_tir))

		




def q(state, action = None):
	if state not in q_table:
		q_table = np.zeros(len(ACTION))

	if action is None:
		return q_table[state]

	return q_table[state][action]



def markov_process(state):
	if (rd.uniform(0,1) < eps): #prob eps de d'exploorer
		return rd.choice(ACTION)
	else:
		return np.argmax(q(state)) 

def calcul_reward(current_state, action):
	next_state = State(agent,objets)








#entrainement de tout les agents
def train():
	list_state = [] 
	list_action = []
	list_total_reward = np.zeros(1,len(list_agent))

	for i in range(N_EPISODE):
		del list_state[:]
		for k in range(len(list_agent)):
			list_state.append(State(list_agent[k],objets)); #Stock les etats de chaque agent

			for j in range(N_STEP):
				for m in range(len(list_state)): # pour chaque etat d'agent choisi une action associé grace a la Q_table
					list_action.append(markov_process(list_state[m]))
				#FAIRE ACTION CHOISI POUR CHAQUE AGENT (UPDATEGAME)
				 
				 ############A FAIRE######################
				

				#CALCUL Reward R pour chaque agent
				for m in range(len(list_agent)):

					list_total_reward[m] = list_total_reward[m] + calcul_reward(list_state[m],list_action[m])



				#CREATION NOUVEL ETAT POUR CHAQUE AGENT










class Game():
	#class pour gerer le jeu
	objectsList = []
	list_agent = []
	# initialisations : 
	# "current" : la valeur utilisee par le jeu
	# "window" : la valeur qui l'utilisateur change a la fenettre
	current_nb_agents_E1 = 0 # equipe 1
	window_nb_agents_E1 = 0
	current_nb_agents_E2 = 0 # equipe 2
	window_nb_agents_E2 = 0
	current_resource_spawn_rate = 0
	window_resource_spawn_rate = 0
	current_learning_rate = 0
	window_learning_rate = 0
	current_random_path_prob = 0 # prob de l'exploration de boltzman
	window_random_path_prob = 0 # prob de l'exploration de boltzman
	current_time_period = 0 # temps entre frames
	window_time_period = 0 # temps entre frames
	current_time_modulo = 0 # pour afficher a chaque X frames
	window_time_modulo = 0 # pour afficher a chaque X frames
	current_nombre_depisodes = 0
	window_nombre_depisodes = 0
	def __init__(self):
		self.list_agent.append(Agent())
	def playPause(self):
		print ("DEBUG play pause")
		pass #TODO
	def reset(self):
		print ("DEBUG reset") # DEBUG
		# actualiser les valeurs
		self.current_nb_agents_E1 = self.window_nb_agents_E1
		self.current_nb_agents_E2 = self.window_nb_agents_E2
		self.current_resource_spawn_rate = self.window_resource_spawn_rate
		self.current_learning_rate = self.window_learning_rate
		self.current_random_path_prob = self.window_random_path_prob
		self.current_time_period = self.window_time_period
		self.current_time_modulo = self.window_time_modulo
		self.current_nombre_depisodes = self.window_nombre_depisodes
		print ("nb_agents_E1: " + str(self.current_nb_agents_E1))
		print("nb_agents_E2 : " + str(self.current_nb_agents_E2))
		print("resource_spawn_rate " + str(self.current_resource_spawn_rate))
		print("learning_rate" + str(self.current_learning_rate))
		print("random_path_prob : " + str(self.current_random_path_prob))
		print("time_period " + str(self.current_time_period))
		print("time_modulo : " + str(self.current_time_modulo))
		print("nombre_depisodes : " + str(self.current_nombre_depisodes))
		pass #TODO
	def update(self):
	# appellee a chaque frame
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
		# "loop" du jeu
		# print("DEBUG timeout") #debug
		game.update()
		fenetre.update()

	timer = QTimer()
	timer.timeout.connect(timeout)
	timer.start(100)
	
sys.exit(app.exec_())

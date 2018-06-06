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

# AGENT
## Modifié pour commencer avec AGENT_
AGENT_PV_INITIAL = 3
AGENT_WIDTH = 64
AGENT_HEIGHT = 64
AGENT_VITESSE = 10
AGENT_DR = np.pi/30

# PROJECTILE
## Modifié pour commencer avec PROJECTILE_
PROJECTILE_DAMAGE = 1
PROJECTILE_WIDTH = 16
PROJECTILE_HEIGHT = 16
PROJECTILE_VITESSE = 30

# RESSOURCE
## Pas modifié, juste organisé
RESOURCE_REWARD = 400



# TEAM
## Modifié pour commencer avec TEAM_
TEAM_BLUE = 1
TEAM_RED = 2

# IMAGEPATHS
IMAGEPATH_404 = "Images/ImageNotFound.png"
IMAGEPATH_AGENT_BLEU = "Images/AgentBleu.png"
IMAGEPATH_AGENT_ROUGE = "Images/AgentRouge.png"
IMAGEPATH_AGENT_NEUTRE = "Images/AgentNeutre.png"

#Action possible
## Modifié pour commencer avec ACTION_
ACTION_STOP = 0
ACTION_MOVE = 1
ACTION_TRIGO = 2
ACTION_HORAIRE = 3
ACTION_SHOOT = 4
ACTION_BUILD = 5
ACTIONS = [ACTION_STOP,ACTION_MOVE,ACTION_TRIGO,ACTION_HORAIRE,ACTION_SHOOT,ACTION_BUILD]



#TYPE
## Modifié pour commencer avec TYPE
TYPE_AGENT = 1
TYPE_TIR = 2
TYPE_RESOURCE = 0

#TRAINING
## Modifié pour commencer avec TRAINING_
TRAINING_EPISODE = 100
TRAINING_STEP = 10
TRAINING_GAMMA = 0.5

# ???
H = 256
W = 256

#N_STATE = len([0:np.sqrt(H*H+W*W):])
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
	pixmap = None
	def __init__(self,x=0,y=0, dx=0, dy=0 ,angle = 0, team = 0,type_obj = 0):
		self.x = x;
		self.y = y;
		self.dx = dx;
		self.dy = dy;
		self.angle = angle
		self.team = team
		self.type_obj = type_obj
		pixmapPath = IMAGEPATH_404
		
		if type_obj == TYPE_RESOURCE:
			#ressource
			pass
		elif type_obj == TYPE_AGENT:
			#L'objet est un agent
			if team == TEAM_BLUE:
				#Agent bleu
				pixmapPath = IMAGEPATH_AGENT_BLEU
			elif team == TEAM_RED:
				#Agent rouge
				pixmapPath = IMAGEPATH_AGENT_ROUGE
			else:
				#Agent neutre
				pixmapPath = IMAGEPATH_AGENT_NEUTRE

		elif type_obj == TYPE_PROJECTILE:
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
		if(self.x + self.box_x  >= 500):
			self.x = 500 - self.box_x
		if(self.y + self.box_y  >=500):
			self.y = 500 - self.box_y
			
		return ret
			
	def draw(self, qp):
		#affichage de l'objet
		## Modifié pour inclure la rotation de l'objet
		r = np.deg2rad(self.angle)
		w=0
		h=0
		if self.type_obj == TYPE_RESOURCE:
			w = RESOURCE_WIDTH
			h = RESOURCE_HEIGHT
		elif self.type_obj == TYPE_AGENT:
			w = AGENT_WIDTH
			h = AGENT_HEIGHT
		elif self.type_obj == TYPE_PROJECTILE:
			w = PROJECTILE_WIDTH
			h = PROJECTILE_HEIGHT

		w2 = w/2
		h2 = h/2
		x1 = (self.x + w2)*np.cos(r) + (self.y + h2)*np.sin(r) - w2
		y1 = -(self.x + w2)*np.sin(r) + (self.y + h2)*np.cos(r) - h2
		qp.rotate(self.angle)
		qp.drawPixmap(x1,y1, 64, 64, self.pixmap); #peut-être besoin de W et H
		qp.rotate(-self.angle)
		

		
class Agent(Objet):
# classe pour les agents
	current_action = 0
	def __init__(self,x=0,y=0, dx=0, dy=0, angle = 0, team = 0):
		Objet.__init__(self,x,y,dx,dy,angle,team, TYPE_AGENT);
		self.pv = AGENT_PV_INITIAL

	def shoot(self):
		Tir(agent)
		
	def action(self, state):
	# prendre une action
		
		if (current_action == ACTION_STOP):
			pass
		
		if (current_action == ACTION_MOVE):
			self.dy =  int(round(AGENT_VITESSE*sin(agent.angle))) #maj des prochains dépacment
			self.dx = int(round(AGENT_VITESSE*cos(agent.angle)))

		if (current_action == ACTION_TRIGO):
			self.angle = angle + AGENT_DR
		if (current_action == ACTION_HORAIRE):
			self.angle = angle - AGENT_DR
		
		if(current_action == ACTION_SHOOT):
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
		self.dy =  int(round(PROJECTILE_VITESSE*sin(agent.angle))) #maj des prochains dépacment
		self.dx = int(round(PROJECTILE_VITESSE*cos(agent.angle)))
		Objet.__init__(self,agent.x,agent.y,dx,dy,agent.team,agent.angle, 0, TYPE_TIR);
		self.dmg = PROJECTILE_DAMAGE


		
class Block(Objet):
# classe pour les blocks Mur
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y);
		
class Resource(Objet):
# classe pour les rescources
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y,0,0,0,0,TYPE_RESOURCE);
		self.value =  RESOURCE_VALUE







class State():
	table_angle_ally = []
	table_dist_ally = []
	table_angle_ennemy = []
	table_dist_ennemy = []
	table_angle_tir = []
	table_dist_tir = []
	table_angle_resource = []
	table_dist_resource = []
	def __init__(self,agent,objectsList):
		self.total_pv_ennemy = 0
		for i in objectsList:
			if (i.type == 1): #AGENT DE LA MEME EQUIPE
				if (i.team == agent.team):
					self.table_angle_ally.append(agent.angle(i))
					self.table_dist_ally.append(agent.distance(i))
				else:
					self.table_angle_ennemy.append(agent.angle(i))
					self.table_dist_ennemy.append(agent.distance(i))
					self.total_pv_ennemy = self.total_pv_ennemy + i.pv
			if (i.type == 2): #TIR
				if(i.type == agent.team):
					pass
				else:
					self.table_angle_tir.append(agent.angle(i))
					self.table_dist_tir.append(agent.distance(i))

			if (i.type == 0): #RESOURCE
				self.table_angle_resource.append(agent.angle(i))
				self.table_dist_resource.append(agent.distance(i))
		"""
			if (i.type == 3)#BLOCK
				table_angle_tir.append(agent.angle(i))
				table_dist_tir.append(agent.distance(i))

		"""
		#STATE DEFINITION:
		#position ennemi le plus proche
		self.distance_nearest_ennemy = np.min(self.table_dist_ennemy)
		self.angle_nearest_ennemy = self.table_angle_ennemy(self.table_dist_ennemy.index(self.distance_nearest_ennemy))
		#position moyenne allié
		self.mean_distance_ally = np.mean(self.table_dist_ennemy)
		self.mean_angle_ally = np.mean(self.table_angle_ennemy)
		#position ressource la plus proche
		self.distance_nearest_resource = np.min(self.table_dist_resource)
		self.angle_nearest_resource = self.table_angle_resource(self.table_dist_resource.index(self.distance_nearest_resource))
		#position tir le plus proche
		self.distance_nearest_tir = np.min(self.table_dist_tir)
		self.angle_nearest_tir = self.table_angle_tir(self.table_dist_tir.index(self.distance_nearest_tir))
		#Point de vie
		self.pv = agent.pv
		




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
	next_state = State(agent,Game.objectsList)
	reward = 0
	#si il se rapproche des ressources
	if (next_state.distance_nearest_resource < current_state.distance_nearest_resource):
		reward  = reward + 10
	else:
		reward = reward - 10
	#si un tir ennemy se rapproche de lui
	if (next_state.disance_nearest_tir < current_state.distance_nearest_tir):
		reward = reward - 2
	#si perd pV
	if (next_state.pv < current_state.pv):
		reward = reward - 100
	#si orienté plus justement face a ressource
	if(next_state.angle_nearest_resource < current_state.angle_nearest_resource):
		reward = reward + 2
	# COMPARER les totals rewards de chaque équipe	(a faire)
	if(next_state.total_pv_ennemy < current_state.total_pv_ennemy):
		reward = reward + 100

	return reward , next_state




#entrainement de tout les agents
def train():
	list_state = [] 
	list_action = []
	list_total_reward = np.zeros(1,len(list_agent))

	for i in range(N_EPISODE):
		del list_state[:]
		for k in range(len(list_agent)):
			list_state.append(State(list_agent[k],Game.objectsList)); #Stock les etats de chaque agent

			for j in range(N_STEP):
				for m in range(len(list_state)): # pour chaque etat d'agent choisi une action associé grace a la Q_table
					list_action.append(markov_process(list_state[m]))
					#FAIRE ACTION CHOISI POUR CHAQUE AGENT (UPDATEGAME)
					list_agent[m].current_action = list_action[m] #met a jour l'action de l'agent dans la classe
				 	############A FAIRE######################
				

				#CALCUL Reward R pour chaque agent
				for m in range(len(list_agent)):
					reward , next_state =  calcul_reward(list_state[m],list_action[m])
					list_total_reward[m] = list_total_reward[m] + reward
					#CREATION NOUVEL ETAT POUR CHAQUE AGENT
					q(list_state[m])[list_action[m]] = q(list_state[m] , list_action[m]) + current_learning_rate * (reward + gamma * np.max(q(next_state)) - q(list_state[m],list_action[m]))
					list_state[m] = next_state
					print("Episode: "+ i +"Agent: "+ m +"  Total reward = "+ list_total_reward[m])










class Game():
	#class pour gerer le jeu
	objectsList = []
	list_agent = []
	isPlay = False # flag : False = pause; True = play
	gameCounter = 1 # clock pour time modulo
	# initialisations : 
	# "current" : la valeur utilisee par le jeu
	# "window" : la valeur qui l'utilisateur change a la fenettre
	current_nb_agents_E1 = 1 # equipe 1
	window_nb_agents_E1 = 1
	current_nb_agents_E2 = 0 # equipe 2
	window_nb_agents_E2 = 0
	current_resource_spawn_rate = 0
	window_resource_spawn_rate = 0
	current_learning_rate = 0
	window_learning_rate = 0
	current_random_path_prob = 0 # prob de l'exploration de boltzman
	window_random_path_prob = 0 # prob de l'exploration de boltzman
	current_time_period = 100 # temps entre frames
	window_time_period = 100 # temps entre frames
	current_time_modulo = 1 # pour afficher a chaque X frames
	window_time_modulo = 1 # pour afficher a chaque X frames
	current_nombre_depisodes = 0
	window_nombre_depisodes = 0
	def __init__(self):
		self.creer_agents()

	def creer_agents(self):
		# TODO : refaire
		A1 = Agent(0, 0, 0, 0, 0, 1)
		A2 = Agent(0, 0, 0, 0, 45, 2)
		self.list_agent.append(A1)
		self.list_agent.append(A2)
		self.objectsList.append(A1)
		self.objectsList.append(A2)

	def playPause(self):
		print ("DEBUG play pause")
		self.isPlay = not(self.isPlay) # toggle flag
		pass #TODO ?

	def reset(self):
		print ("DEBUG reset") # DEBUG
		self.isPlay = False # stop the game
		self.objectsList = [] # effacer tous les objets
		self.list_agent = []
		# actualiser les valeurs
		self.current_nb_agents_E1 = self.window_nb_agents_E1
		self.current_nb_agents_E2 = self.window_nb_agents_E2
		self.current_resource_spawn_rate = self.window_resource_spawn_rate
		self.current_learning_rate = self.window_learning_rate
		self.current_random_path_prob = self.window_random_path_prob
		self.current_time_period = self.window_time_period
		self.current_time_modulo = self.window_time_modulo
		self.current_nombre_depisodes = self.window_nombre_depisodes
		"""
		print ("nb_agents_E1: " + str(self.current_nb_agents_E1))
		print("nb_agents_E2 : " + str(self.current_nb_agents_E2))
		print("resource_spawn_rate " + str(self.current_resource_spawn_rate))
		print("learning_rate" + str(self.current_learning_rate))
		print("random_path_prob : " + str(self.current_random_path_prob))
		print("time_period " + str(self.current_time_period))
		print("time_modulo : " + str(self.current_time_modulo))
		print("nombre_depisodes : " + str(self.current_nombre_depisodes))
		"""
		self.creer_agents()
		ui.gameWidget.update()
		pass #TODO ?
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
		if(game.isPlay):
			# "loop" du jeu
			# print("DEBUG timeout") #debug
			game.update()
			if((game.gameCounter%game.current_time_modulo)==0):
				ui.gameWidget.update()
		game.gameCounter += 1

	timer = QTimer()
	timer.timeout.connect(timeout)
	timePeriod = ui.SpinBoxTimePeriod.value()
	timer.start(timePeriod)
	
sys.exit(app.exec_())

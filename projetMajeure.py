#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# PROJET MAJEURE - Reinforcement Learning
# ERBACHER, Pierre
# FOLETTO PIMENTA, Pedro
# TIZON, Nicolas

import sys
import time
#import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer
from interface import *
from state import *
import numpy as np
import random as rd
import math
from os import system as osSystem

# WINDOW / GAME_AREA
## Modifié pour commencer avec WINDOW_, GAME_AREA_
# ATTENTION : Ces variables sont également définies dans projetMajeure.py.
# Pensez à les modifier là-bas aussi ou à faire une variable partagée

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 500

# AGENT
## Modifié pour commencer avec AGENT_
AGENT_PV_INITIAL = 3
AGENT_WIDTH = 32
AGENT_HEIGHT = 32
AGENT_VITESSE = 10
NB_AGENTS_BLEUS = 4
NB_AGENTS_ROUGES = 2
#AGENT_DR = np.pi/30
AGENT_DR = 5 #en degrés

# PROJECTILE
## Modifié pour commencer avec PROJECTILE_
PROJECTILE_DAMAGE = 1
PROJECTILE_WIDTH = 8
PROJECTILE_HEIGHT = 8
PROJECTILE_VITESSE = 20

# RESSOURCE
## Pas modifié, juste organisé
RESOURCE_WIDTH = 24
RESOURCE_HEIGHT = 24
RESOURCE_REWARD = 400
NB_MAX_RESOURCES = 3

global startTime
startTime = 0


# TEAM
## Modifié pour commencer avec TEAM_
TEAM_BLUE = 1
TEAM_RED = 2

# IMAGEPATHS
IMAGEPATH_404 = "Images/ImageNotFound.png"
IMAGEPATH_AGENT_BLEU = "Images/AgentBleu.png"
IMAGEPATH_AGENT_ROUGE = "Images/AgentRouge.png"
IMAGEPATH_AGENT_NEUTRE = "Images/AgentNeutre.png"
IMAGEPATH_RESOURCE = "Images/Resource2.png"
IMAGEPATH_PROJECTILE_BLEU = "Images/Projectile_Bleu.png"
IMAGEPATH_PROJECTILE_ROUGE = "Images/Projectile_Rouge.png"

#Action possible
## Modifié pour commencer avec ACTION_
"""
ACTION_STOP = 0
ACTION_MOVE = 1
ACTION_TRIGO = 2
ACTION_HORAIRE = 3
ACTION_SHOOT = 4
ACTION_BUILD = 5
"""

ACTION_STOP = 5
ACTION_MOVE = 0
ACTION_TRIGO = 1
ACTION_HORAIRE = 2
ACTION_SHOOT = 3
ACTION_BUILD = 8008135
ACTIONS = [ACTION_MOVE,ACTION_TRIGO,ACTION_HORAIRE, ACTION_SHOOT]



#TYPE
## Modifié pour commencer avec TYPE
TYPE_RESOURCE = 0
TYPE_AGENT = 1
TYPE_PROJECTILE = 2
TYPE_BLOCK = 3

#TRAINING
## Modifié pour commencer avec TRAINING_
TRAINING_N_EPISODE = 500
TRAINING_N_STEP = 750
TRAINING_GAMMA = 0.95
TRAINING_LEARNING_RATE = 0.01

#N_STATE = len([0:np.sqrt(H*H+W*W):])
global q_table_E1, q_table_E2
q_table_E1 = {} #equipe bleu
q_table_E2 = {} #equipe rouge
eps = 0.05

global total_reward_bleu, total_reward_rouge
total_reward_bleu = []
total_reward_rouge = []

class Objet:
# classe pour tout les object qui sont dans l'environnement
	x = 0 # valeur par default
	y = 0
	dx = 0 # vitesses
	dy = 0
	angle = 0
	width = 5 #collision boxes ( largeur et longeur de l'objet)
	height = 5
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
		self.width = 32
		self.height = 32
		
		if type_obj == TYPE_RESOURCE:
			#ressource
			self.width = RESOURCE_WIDTH
			self.height = RESOURCE_HEIGHT
			pixmapPath = IMAGEPATH_RESOURCE
		elif type_obj == TYPE_AGENT:
			#L'objet est un agent
			self.width = AGENT_WIDTH
			self.height = AGENT_HEIGHT
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
			self.width = PROJECTILE_WIDTH
			self.height = PROJECTILE_HEIGHT
			if team == TEAM_BLUE:
				#Agent bleu
				pixmapPath = IMAGEPATH_PROJECTILE_BLEU
			elif team == TEAM_RED:
				#Agent rouge
				pixmapPath = IMAGEPATH_PROJECTILE_ROUGE

		self.pixmap = QPixmap()
		self.pixmap.load(pixmapPath)	
			
	def move(self):
	# bouger l'agent et tir d'accord avec sa vitesse
		#self.x = min(max(0,self.x + self.dx), GAME_AREA_WIDTH - self.pixmap.width())
		#self.y = min(max(0,self.y + self.dy), GAME_AREA_HEIGHT - self.pixmap.height())
		self.x = max(0,self.x + self.dx)
		self.y = max(0,self.y + self.dy)
		if(self.x + self.width  >= GAME_AREA_WIDTH):
			self.x = GAME_AREA_WIDTH - self.width
		if(self.y + self.height  >=GAME_AREA_HEIGHT):
			self.y = GAME_AREA_HEIGHT - self.height
	
	def collision(self,obj):
		#verifie la collision entre les objets
		ret = False
		#if (self.x + self.width < obj.x - obj.width and self.x - self.width > obj.x + obj.width and self.y + self.height < obj.y - obj.height and self.y - self.height > obj.y + obj.height):
		if ((self.x + self.width < obj.x or self.x > obj.x + obj.width) or (self.y + self.height < obj.y or self.y > obj.y + obj.height)):
    			ret = False
		else:
			ret = True

			
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
		qp.drawPixmap(x1,y1, w, h, self.pixmap); #peut-être besoin de W et H
		qp.rotate(-self.angle)
		

		
class Agent(Objet):
# classe pour les agents
	current_action = 0
	aTire = False
	aMange = False
	estTouche = False
	estMort = False
	cibleTouchee = False
	def __init__(self,x=0,y=0, angle = 0, team = 0):
		dx = 0
		dy = 0
		Objet.__init__(self,x,y,dx,dy,angle,team, TYPE_AGENT);
		self.pv = AGENT_PV_INITIAL
		self.reload = 0
		self.reloadMax = 4
		self.aMange = False
		self.estTouche = False
		self.estMort = False
		self.cibleTouchee = False
		self.pommesMangees = 0
		self.victimes = 0

	def shoot(self):
		if self.reload == 0:
			self.aTire = True
			self.reload = self.reloadMax
			projectile = Tir(self)
			game.objectsList.append(projectile)
			game.list_projectile.append(projectile)

	def takeDamage(self, p):
		self.pv = self.pv - p.dmg
		self.estTouche = True
		if self.pv < 0:
			self.spawn()
			self.estMort = True
			p.agent.victimes = p.agent.victimes+1
	
	def spawn(self):
		angle = rd.randint(0,360)
		if self.team == 1: #BLEU
			x = rd.randint(0,100-AGENT_WIDTH)
			y = rd.randint(0,GAME_AREA_HEIGHT-AGENT_HEIGHT)
		elif self.team == 2: #ROUGE
			x = rd.randint(GAME_AREA_WIDTH-100,GAME_AREA_WIDTH-AGENT_WIDTH)
			y = rd.randint(0,GAME_AREA_HEIGHT-AGENT_HEIGHT)
		else:
			print("ERR: INCORRECT AGENT")

		self.x = x
		self.y = y
		self.angle = angle
		self.pv = AGENT_PV_INITIAL
			
		
	def execute_action(self, state):
	# faire une action
		#self.current_action = self.take_action(state) # choisir l'action
		if (self.current_action == ACTION_STOP):
			self.dy = 0
			self.dx = 0
		elif (self.current_action == ACTION_MOVE):
			self.dy =  int(round(-AGENT_VITESSE*np.cos(np.deg2rad(self.angle)))) #maj des prochains dépacment
			self.dx = int(round(AGENT_VITESSE*np.sin(np.deg2rad(self.angle))))
		elif (self.current_action == ACTION_TRIGO):
			self.dy = 0
			self.dx = 0
			self.angle = self.angle - AGENT_DR
			if (self.angle < -360):
				self.angle = self.angle + 360
		elif (self.current_action == ACTION_HORAIRE):
			self.dy = 0
			self.dx = 0
			self.angle = self.angle + AGENT_DR
			if (self.angle > 360):
				self.angle = self.angle - 360
		elif(self.current_action == ACTION_SHOOT):
			self.dy = 0
			self.dx = 0
			self.shoot()
		else:
			print("ERR: INCORRECT ACTION BEING EXECUTED")
			
	"""
	def take_action(self, state):
	# choisir une action
		# TODO
		# comportement temporaire : 
		rdm_prob = rd.uniform(0,1)
		if (rdm_prob < 0.10): # 10%
			return ACTION_MOVE
		elif (rdm_prob < 0.40): #30%
			return ACTION_TRIGO
		elif (rdm_prob < 0.90): #50%
			return ACTION_HORAIRE
		elif (rdm_prob < 0.95): #5%
			return ACTION_SHOOT
		else : #5%
			return ACTION_STOP
	"""
		
		

	def distanceWithObj(self,objet):
		return np.sqrt((objet.x - self.x)*(objet.x - self.x) + (objet.y - self.y)*(objet.y - self.y))

	def angleWithObj(self,objet):
		a = np.rad2deg(math.atan2( objet.x - self.x, -objet.y + self.y)) - self.angle
		if (a > 180):
			a = a - 360
		if (a < -180):
			a = a + 360
		return a

	def place_block(self):
	# placer un bloque en face du agent
		pass # TODO
	
class Tir(Objet):
# classe pour les tirs
	def __init__(self,agent):
		self.dy =  int(round(-PROJECTILE_VITESSE*np.cos(np.deg2rad(agent.angle)))) #maj des prochains dépacment
		self.dx = int(round(PROJECTILE_VITESSE*np.sin(np.deg2rad(agent.angle))))
		Objet.__init__(self,agent.x,agent.y,self.dx,self.dy,agent.angle,agent.team,TYPE_PROJECTILE)
		self.x = agent.x + agent.width/2 - self.width/2
		self.y = agent.y + agent.height/2 - self.height/2
		self.dmg = PROJECTILE_DAMAGE
		self.agent = agent
	def move(self):
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		# si le tir sort l'ecran il disparait
		#if(self.x + self.width  >= GAME_AREA_WIDTH or self.y + self.height >= GAME_AREA_HEIGHT or self.x < 0 or self.y < 0):
		#	game.objectsList.remove(self)
		#	game.list_projectile.remove(self)
		


		
class Block(Objet):
# classe pour les blocks Mur
	def __init__(self,x=0,y=0):
		Objet.__init__(self,x,y,0,0,0,0,TYPE_BLOCK);
		
class Resource(Objet):
# classe pour les rescources
	def __init__(self,x=0,y=0):
		Objet.__init__(self,x,y,0,0,0,0,TYPE_RESOURCE);
		self.reward =  RESOURCE_REWARD
		
def q(state, action = None, team = 0):
	global q_table_E1, q_table_E2

	if team == 1: # EQUIPE BLEU
		q_table = q_table_E1
	elif team == 2: # EQUIPE ROUGE
		q_table = q_table_E2
	else: # error
		print("ERROR in q function : equipe doit etre 1 ou 2")
		return

	if state.stateID not in q_table.keys():
		q_table[state.stateID] = [0 for i in ACTIONS]
	if action is None:
		return q_table[state.stateID]

	return q_table[state.stateID][action]



def markov_process(state, agent, isTraining):
	if (isTraining and rd.uniform(0,1) < eps):
		return rd.choice(ACTIONS)
	else:
		qt = q(state, team=agent.team)
		actions = np.argwhere(qt == np.amax(qt))
		a = rd.choice(actions)
		a = a[0]
		return a

def calcul_reward(current_state,next_state):

	reward = 0

	agent = next_state.agent


	#AGENT BLEU
	#Récompensé pour manger des ressources
	#Aucune récompense pour tuer l'adversaire
	#Pénalisé pour être blessé

	if agent.team == 1:

		#A Mangé
		if(next_state.agent.aMange):
			reward = reward + 150
			#print(agentName + " a mangé")
		
		#A Tiré
		if(agent.aTire):
			reward = reward - 10
		"""
		#Distance Ressource
		d = (current_state.D_resource_min - next_state.D_resource_min - 2)
		reward = reward - d
		"""
		"""
		#Angle Ressource
		if(abs(next_state.A_resource_min) < abs(current_state.A_resource_min) and not agent.estMort):
			reward = reward + 2
		elif(abs(next_state.A_resource_min) > abs(current_state.A_resource_min) and not agent.estMort):
			reward = reward - 2
		else:
			reward = reward - 0.02

		#Distance Ennemi
		if (next_state.D_ennemy_min < current_state.D_ennemy_min and not agent.estMort):
			reward  = reward + 5
		elif (next_state.D_ennemy_min > current_state.D_ennemy_min and not agent.estMort):
			reward = reward - 5
		else:
			reward = reward - 0.05

		#Angle Ennemi
		if (next_state.A_ennemy_min > current_state.A_ennemy_min and not agent.estMort):
			reward  = reward + 1
		elif (next_state.A_ennemy_min < current_state.A_ennemy_min and not agent.estMort):
			reward = reward - 1
		else:
			reward = reward - 0.01
		"""
		"""
		#Distance Ressource
		if (next_state.S_D_resource_min < current_state.S_D_resource_min and not agent.estMort):
			reward  = reward + 100
		elif (next_state.S_D_resource_min > current_state.S_D_resource_min and not agent.estMort):
			reward = reward - 100
		else:
			reward = reward - 1

		#Angle Ressource
		if(abs(next_state.S_A_resource_min) < abs(current_state.S_A_resource_min) and not agent.estMort):
			reward = reward + 20
		elif(abs(next_state.S_A_resource_min) > abs(current_state.S_A_resource_min) and not agent.estMort):
			reward = reward - 20
		else:
			reward = reward - 0.2

		#Distance Ennemi
		if (next_state.S_D_ennemy_min < current_state.S_D_ennemy_min and not agent.estMort):
			reward  = reward + 50
		elif (next_state.S_D_ennemy_min > current_state.S_D_ennemy_min and not agent.estMort):
			reward = reward - 50
		else:
			reward = reward - 0.5

		#Angle Ennemi
		if (next_state.S_A_ennemy_min > current_state.S_A_ennemy_min and not agent.estMort):
			reward  = reward + 10
		elif (next_state.S_A_ennemy_min < current_state.S_A_ennemy_min and not agent.estMort):
			reward = reward - 10
		else:
			reward = reward - 0.1
	"""
	#AGENT ROUGE
	#Aucune récompense pour manger des ressources
	#Récompensé pour tuer l'ennemi
	#Pénalisé pour être blessé
	elif agent.team == 2:
	
		# Est Touché
		if(next_state.agent.estTouche):
			reward = reward - 200
			#print(agentName + " est touché")

		# Est Mort (touché trois fois)
		if(next_state.agent.estMort):
			reward = reward - 800
			#print(agentName + " est mort")

		# Cible Touchée
		if(next_state.agent.cibleTouchee):
			reward = reward + 500
			#print(agentName + " a touché une cible")
		"""
		#Angle Ennemi
		if(abs(next_state.S_A_ennemy_min) < abs(current_state.S_A_ennemy_min)):
			reward = reward + 50
		elif(abs(next_state.S_A_ennemy_min) > abs(current_state.S_A_ennemy_min)):
			reward = reward - 50
		else:
			reward = reward - 0.5

	
	"""
	"""
	if not game.isTraining:
		if agent.team == 1:
			blueScore = blueScore + reward
		else:
			redScore = redScore + reward
	"""	
	#Réinitialiser les booléennes
	agent.estTouche = False
	agent.estMort = False
	agent.cibleTouchee = False
	agent.aManger = False
	agent.aTire = False
	return reward




#entrainement de tout les agents
def qtrain():
	global q_table_E1, q_table_E2, total_reward_bleu, total_reward_rouge
	
	list_total_reward = [0 for agent in game.list_agent]
	list_action = [None for agent in game.list_agent]
	list_state = [None for agent in game.list_agent]

	total_reward_bleu = [0 for i in range(TRAINING_N_EPISODE)]
	total_reward_rouge = [0 for i in range(TRAINING_N_EPISODE)]
	total_pommes_bleu = [0 for i in range(TRAINING_N_EPISODE)]
	total_pommes_rouge = [0 for i in range(TRAINING_N_EPISODE)]
	total_victimes_bleu = [0 for i in range(TRAINING_N_EPISODE)]
	total_victimes_rouge = [0 for i in range(TRAINING_N_EPISODE)]
	#Pour chaque partie
	for i in range(TRAINING_N_EPISODE):
		# variation du nombre des agents a chaque episode
		#game.window_nb_agents_E1 = rd.randint(1, 5)
		#game.window_nb_agents_E2 = rd.randint(0, 5)
		game.reset()
		#vider les lists
		p = np.floor(1000*i/TRAINING_N_EPISODE)/10
		list_total_reward = [0 for agent in game.list_agent]
		list_action = [None for agent in game.list_agent]
		list_state = [None for agent in game.list_agent]
		osSystem("clear") #Vider la console
		#Message affiché à chaque itération
		runTime = np.floor(time.time() - startTime)
		timeLeft = np.floor((TRAINING_N_EPISODE-i)*(runTime/(i or 1)))

		runTime_h = int(runTime/3600)
		runTime_m = int(runTime/60)%60
		runTime_s = int(runTime%60)

		timeLeft_h = int(timeLeft/3600)
		timeLeft_m = int(timeLeft/60)%60
		timeLeft_s = int(timeLeft%60)

		runTime_h = (runTime_h < 10 and "0" or " ") + str(runTime_h)
		runTime_m = (runTime_m < 10 and ":0" or ":") + str(runTime_m)
		runTime_s = (runTime_s < 10 and ":0" or ":") + str(runTime_s)
		timeLeft_h = (timeLeft_h < 10 and "0" or " ") + str(timeLeft_h)
		timeLeft_m = (timeLeft_m < 10 and ":0" or ":") + str(timeLeft_m)
		timeLeft_s = (timeLeft_s < 10 and ":0" or ":") + str(timeLeft_s)

		
		print("Entrainement en cours...")
		print("Episode : " + str(i) + "/" + str(TRAINING_N_EPISODE))
		print("(" + str(p) + "%)")
		print("Time elapsed: " + runTime_h + runTime_m + runTime_s)
		print("Estimated time left: " + timeLeft_h + timeLeft_m + timeLeft_s)
		print("\nQ_table sizes:")
		print("BLUE: " + str(len(q_table_E1.keys())) + "		RED: " + str(len(q_table_E2.keys())))

		#initialisation ETAT agent
		for k in range(len(game.list_agent)):
			list_state[k] = State(game.list_agent[k],game.objectsList); #Stock les etats de chaque agent
		#Debut partie		
		for j in range(TRAINING_N_STEP):
			list_action = takeAllActions(list_state)
			game.update()
			updateQTable(list_state, list_action, list_total_reward)

		#stockage des total rewards
		for k in range(len(game.list_agent)):

			if game.list_agent[k].team == 1: # BLEU
				total_reward_bleu[i] = total_reward_bleu[i] + list_total_reward[k]
				total_pommes_bleu[i] = total_pommes_bleu[i] + game.list_agent[k].pommesMangees
				total_victimes_bleu[i] = total_victimes_bleu[i] + game.list_agent[k].victimes
			elif game.list_agent[k].team == 2: # ROUGE
				total_reward_rouge[i] = total_reward_rouge[i] + list_total_reward[k]
				total_pommes_rouge[i] = total_pommes_rouge[i] + game.list_agent[k].pommesMangees
				total_victimes_rouge[i] = total_victimes_rouge[i] + game.list_agent[k].victimes

	#print("R_bleu = " + str(total_reward_bleu))
	#print("R_rouge = " + str(total_reward_rouge))
	print("P_bleu = " + str(total_pommes_bleu))
	print("P_rouge = " + str(total_pommes_rouge))
	print("V_bleu = " + str(total_victimes_bleu))
	print("V_rouge = " + str(total_victimes_rouge))

def takeAllActions(list_state):
 # pour chaque etat d'agent choisi une action associé grace a la Q_table
	list_action = [None for agent in game.list_agent]
	for m in range(len(list_state)):
		list_action[m] = markov_process(list_state[m], game.list_agent[m], True)
		game.list_agent[m].current_action = list_action[m] #met a jour l'action de l'agent dans la classe
		game.list_agent[m].execute_action(list_state[m])
	return list_action


def updateQTable(list_state, list_action, list_total_reward):
	current_learning_rate = TRAINING_LEARNING_RATE #0.001 #A changer
	for m in range(len(game.list_agent)):
		# get agent team
		team = list_state[m].agent.team
		
		#CALCUL les nouvelles etats
		next_state = State(list_state[m].agent,game.objectsList)
		#CALCUL Reward R pour chaque agent
		reward =  calcul_reward(list_state[m],next_state)
		#print("debug updateQtable : " + str(m) + " reward : " + str(reward))
		list_total_reward[m] = list_total_reward[m] + reward
		#CREATION NOUVEL ETAT POUR CHAQUE AGENT
		#q(list_state[m])[list_action[m]] = (1-current_learning_rate)*q(list_state[m] , list_action[m]) + current_learning_rate * (reward + TRAINING_GAMMA * max(q(next_state)) - q(list_state[m],list_action[m]))
		#q(list_state[m], team=team)[list_action[m]] = (1-current_learning_rate)*q(list_state[m] , list_action[m], team=team) + current_learning_rate * (reward + TRAINING_GAMMA * max(q(next_state,team=team)) - q(list_state[m],list_action[m],team=team))
		#pb de 1-2lambda
		q(list_state[m], team=team)[list_action[m]] = (1-current_learning_rate)*q(list_state[m] , list_action[m], team=team) + current_learning_rate * (reward + TRAINING_GAMMA * max(q(next_state,team=team)))
		#q(list_state[m])[list_action[m]]
		list_state[m] = next_state
		#print("Agent: "+ str(m) +"  Total reward = "+ str(list_total_reward[m]))


def save_q_tables():
	global q_table_E1, q_table_E2
	np.save('q_table_E1.npy', q_table_E1) 
	np.save('q_table_E2.npy', q_table_E2)
	print("saved Q-tables")

def load_q_tables():
	global q_table_E1, q_table_E2
	q_table_E1 = np.load('q_table_E1.npy').item()
	q_table_E2 = np.load('q_table_E2.npy').item()
	print("loaded Q-tables")







class Game():
	#class pour gerer le jeu
	objectsList = []
	list_agent = []
	list_resource = []
	list_projectile = []
	isPlay = False # flag : False = pause; True = play
	isTraining = False
	gameCounter = 1 # clock pour time modulo
	# initialisations : 
	# "current" : la valeur utilisee par le jeu
	# "window" : la valeur qui l'utilisateur change a la fenettre
	current_nb_agents_E1 = NB_AGENTS_BLEUS # equipe 1
	window_nb_agents_E1 = NB_AGENTS_BLEUS
	current_nb_agents_E2 = NB_AGENTS_ROUGES # equipe 2
	window_nb_agents_E2 = NB_AGENTS_ROUGES
	current_resource_spawn_rate = 0.02
	window_resource_spawn_rate = 0.02
	current_learning_rate = TRAINING_LEARNING_RATE
	window_learning_rate = TRAINING_LEARNING_RATE
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
		for i in range(3):
			self.creer_resource()

	def creer_resource(self):
		x = rd.randint(100, GAME_AREA_WIDTH - RESOURCE_WIDTH - 100)
		y = rd.randint(0, GAME_AREA_WIDTH  - RESOURCE_WIDTH)
		resource = Resource(x,y)
		self.objectsList.append(resource)
		self.list_resource.append(resource)

	def creer_agents(self):
		for i in range(self.current_nb_agents_E1):
			a = Agent(0,0,0,1)
			a.spawn()
			self.objectsList.append(a)
			self.list_agent.append(a)

		for i in range(self.current_nb_agents_E2):
			a = Agent(0,0,0,2)
			a.spawn()
			self.objectsList.append(a)
			self.list_agent.append(a)


	def playPause(self):
		#print ("DEBUG play pause")
		self.isPlay = not(self.isPlay) # toggle flag
		pass #TODO ?

	def reset(self):
		#global blueScore, redScore
		self.gameCounter = 0
		#blueScore = 0
		#redScore = 0
		#print ("DEBUG reset") # DEBUG
		self.isPlay = False # stop the game
		self.objectsList = [] # effacer tous les objets
		self.list_agent = []
		self.list_resource = []
		self.list_projectile = []
		# actualiser les valeurs
		self.current_nb_agents_E1 = self.window_nb_agents_E1
		self.current_nb_agents_E2 = self.window_nb_agents_E2
		self.current_resource_spawn_rate = self.window_resource_spawn_rate
		self.current_learning_rate = self.window_learning_rate
		self.current_random_path_prob = self.window_random_path_prob
		self.current_time_period = self.window_time_period
		self.current_time_modulo = self.window_time_modulo
		self.current_nombre_depisodes = self.window_nombre_depisodes
		#debug
		if False:
			print ("nb_agents_E1: " + str(self.current_nb_agents_E1))
			print("nb_agents_E2 : " + str(self.current_nb_agents_E2))
			print("resource_spawn_rate " + str(self.current_resource_spawn_rate))
			print("learning_rate" + str(self.current_learning_rate))
			print("random_path_prob : " + str(self.current_random_path_prob))
			print("time_period " + str(self.current_time_period))
			print("time_modulo : " + str(self.current_time_modulo))
			print("nombre_depisodes : " + str(self.current_nombre_depisodes))
		self.creer_agents()
		for i in range(NB_MAX_RESOURCES):
			self.creer_resource()
		if not self.isTraining:
			ui.gameWidget.update()

	def update_parametres(self):
		self.window_nb_agents_E1 = ui.spinBoxE1.value()
		self.window_nb_agents_E2 = ui.spinBoxE2.value()
		#self.window_resource_spawn_rate = ui.SpinBoxRSR.value()
		#self.window_learning_rate = ui.SpinBoxLearningRate.value()
		#self.window_random_path_prob = ui.SpinBoxRPP.value()
		self.window_time_period = ui.SpinBoxTimePeriod.value()
		self.window_time_modulo = ui.spinBoxModulo.value()
		self.current_nb_agents_E1 = self.window_nb_agents_E1
		self.current_nb_agents_E2 = self.window_nb_agents_E2
		self.current_resource_spawn_rate  = self.window_resource_spawn_rate
		self.current_learning_rate = self.window_learning_rate
		self.current_random_path_prob = self.window_random_path_prob
		self.current_time_period = self.window_time_period
		self.current_time_modulo = self.window_time_modulo

	def update(self):
		if not self.isTraining:
			for agent in self.list_agent:
				state = State(agent, self.objectsList)
				action = markov_process(state, agent, False)
				agent.current_action = action
				agent.execute_action(state)
		
		# mouvement des agents et tirs
		for objet in self.objectsList:
			objet.move()

		#rechargement agents
		for agent in self.list_agent:
			agent.reload = agent.reload-1
			if agent.reload < 0:
				agent.reload = 0

		# collision agent-ressource
		for agent in self.list_agent:
			for resource in self.list_resource:
				if agent.collision(resource):
					self.list_resource.remove(resource)
					self.objectsList.remove(resource)
					#TODO : donner récompense à Agent
					agent.aMange = True
					agent.pommesMangees = agent.pommesMangees + 1
		# collision tir-agent
		for agent in self.list_agent:
			for p in self.list_projectile:
				if agent.collision(p) and agent.team != p.team:
					p.agent.cibleTouchee = True
					agent.takeDamage(p)
					self.objectsList.remove(p)
					self.list_projectile.remove(p)
					continue

		#projectiles sortant du terrain
		for p in self.list_projectile:
			if(p.x + p.width  >= GAME_AREA_WIDTH or p.y + p.height >= GAME_AREA_HEIGHT or p.x < 0 or p.y < 0):
				self.objectsList.remove(p)
				self.list_projectile.remove(p)

		# Ajoute des ressources
		while len(self.list_resource) < NB_MAX_RESOURCES:
			self.creer_resource()



		
# main
if __name__ == '__main__':

	def timeout():
		if(game.isPlay):
			# "loop" du jeu
			game.update()
			if((game.gameCounter%game.current_time_modulo)==0):
				ui.gameWidget.update()
			game.gameCounter += 1
			osSystem("clear")
			print("STEP : " + str(game.gameCounter))
			#print("BLUE SCORE : " + str(blueScore))
			#print("RED SCORE : " + str(redScore))
		#timer.stop()
		timePeriod = game.current_time_period
		#timer.start(timePeriod)
    
	app = QApplication(sys.argv)
	game = Game()
	if "-l" in sys.argv:
		load_q_tables()
	if "-t" in sys.argv:
		game.isTraining = True
		startTime = time.time()
		qtrain()
		save_q_tables()
		#plt.plot(np.linspace(1,TRAINING_N_EPISODES,TRAINING_N_EPISODES,dtype = int), total_reward_bleu)
		#plt.plot(np.linspace(1,TRAINING_N_EPISODES,TRAINING_N_EPISODES,dtype = int), total_reward_rouge)
		#plt.show()
		sys.exit()
	else:
		fenetre = Fenetre(game)
		ui = Ui_MainWindow() # classe cree par QtDesigner
		ui.setupUi(fenetre)
		game.update_parametres()
		osSystem("clear")
		timer = QTimer()
		timer.timeout.connect(timeout)
		timePeriod = ui.SpinBoxTimePeriod.value()
		timer.start(timePeriod)
sys.exit(app.exec_())
	

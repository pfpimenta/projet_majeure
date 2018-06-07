#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# PROJET MAJEURE - Reinforcement Learning
# ERBACHER, Pierre
# FOLETTO PIMENTA, Pedro
# TIZON, Nicolas

import sys
import time
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPixmap
from PyQt5.QtCore import Qt, QTimer


class State():
	table_A_ally = []
	table_D_ally = []
	table_A_ennemy = []
	table_D_ennemy = []
	table_A_projectile = []
	table_D_projectile = []
	table_A_resource = []
	table_D_resource = []
	primes = [2, 3, 5, 7, 11, 13, 17, 19]
	"""
	thresholds = {"D_ennemy_min": [20, 80, 150, 250, 400, 1000],
			"A_ennemy_min": [-180, -90, -50, -20, -5, 0, 5, 20, 50, 90, 180],
			"D_resource_min": [20, 80, 150, 250, 400, 1000],
			"A_resource_min": [-180, -90, -50, -20, -5, 0, 5, 20, 50, 90, 180],
			"D_projectile_min": [20, 80, 150, 250, 400, 1000],
			"A_projectile_min": [-180, -90, -50, -20, -5, 0, 5, 20, 50, 90, 180]}
	"""
	
	thresholds = {"D_ennemy_min": [30, 80, 150, 250, 400, 1000],
			"D_resource_min": [30, 80, 150, 250, 400, 1000],
			"D_projectile_min": [30, 80, 150, 250, 400, 1000],
			"A_ennemy_min": [-100, -80, -10, 10, 80, 100],
			"A_resource_min": [-100, -80, -10, 10, 80, 100]}
	
	def __init__(self,agent,objectsList):
		#self.total_pv_ennemy = 0
		self.agent = agent
		#Mise à vide des listes. Ca marchait pas autrement
		#self.table_D_ally = []
		#self.table_A_ally = []
		self.table_D_ennemy = []
		self.table_A_ennemy = []
		self.table_D_tir = []
		#self.table_A_tir = []
		self.table_D_resource = []
		self.table_A_resource = []

		for i in objectsList:
			if (i.type_obj == 1): #AGENT DE LA MEME EQUIPE
				if (i.team == agent.team):
					pass
					#self.table_A_ally.append(agent.angleWithObj(i))
					#self.table_D_ally.append(agent.distanceWithObj(i))
				else:
					self.table_A_ennemy.append(agent.angleWithObj(i))
					self.table_D_ennemy.append(agent.distanceWithObj(i))
					#self.total_pv_ennemy = self.total_pv_ennemy + i.pv
			if (i.type_obj == 2): #TIR
				if(i.team == agent.team):
					pass
				else:
					#self.table_A_tir.append(agent.angleWithObj(i))
					self.table_D_tir.append(agent.distanceWithObj(i))

			if (i.type_obj == 0): #RESOURCE
				self.table_A_resource.append(agent.angleWithObj(i))
				self.table_D_resource.append(agent.distanceWithObj(i))
			"""
			if (i.type_obj == 3)#BLOCK
				table_A_tir.append(agent.angleWithObj(i))
				table_D_tir.append(agent.distanceWithObj(i))
			"""
		
		#STATE DEFINITION: #variables discretisees
		self.S_D_ennemy_min = 0
		self.S_A_ennemy_min = 0
		self.S_D_resource_min = 0
		self.S_A_resource_min = 0
		self.S_D_projectile_min = 0
		#self.S_A_projectie_min = 0
		#self.state_pv = 0
		#self.state_total_pv_ennemy = 0

		#position ennemi le plus proche
		if(len(self.table_D_ennemy) > 0): # s'il y a un ennemy
			d = min(self.table_D_ennemy)
			self.D_ennemy_min = d
			self.A_ennemy_min = self.table_A_ennemy[self.table_D_ennemy.index(d)]
		else:
			self.D_ennemy_min = 1000
			self.A_ennemy_min = 0
		#position moyenne allié
		#if(len(self.table_dist_ally) > 0): # s'il y a un ally
			#self.mean_distance_ally = sum(self.table_dist_ally)/len(self.table_dist_ally)
			#self.mean_angle_ally = sum(self.table_angle_ally)/len(self.table_dist_ally)
		#else:
			#self.mean_distance_ally = 1000
			#self.mean_angle_ally = 0
		#position ressource la plus proche
		if(len(self.table_D_resource) > 0): # s'il y a un resource
			self.D_resource_min = min(self.table_D_resource)
			self.A_resource_min = self.table_A_resource[self.table_D_resource.index(self.D_resource_min)]
		else:
			self.D_resource_min = 1000
			self.A_resource_min = 0
		#position tir le plus proche
		if(len(self.table_D_projectile) > 0): # s'il y a un tir
			self.D_projectile_min = min(self.table_D_projectile)
			self.A_projectile_min = self.table_A_projectile[self.table_D_projectile.index(self.D_projectile_min)]
		else:
			self.D_projectile_min = 1000
			self.A_projectile_min = 0
		#Point de vie
		self.pv = agent.pv


		self.stateID = 1

		for k in self.thresholds["D_ennemy_min"]:
			if self.D_ennemy_min <= k:
				self.S_D_ennemy_min = self.thresholds["D_ennemy_min"].index(k)
				self.stateID = self.stateID * (self.primes[0]**self.S_D_ennemy_min)
				break
		for k in self.thresholds["A_ennemy_min"]:
			if self.A_ennemy_min <= k:
				self.S_A_ennemy_min = self.thresholds["A_ennemy_min"].index(k)
				self.stateID = self.stateID * (self.primes[1]**self.S_A_ennemy_min)
				break
		for k in self.thresholds["D_resource_min"]:
			if self.D_resource_min <= k:
				self.S_D_resource_min = self.thresholds["D_resource_min"].index(k)
				self.stateID = self.stateID * (self.primes[2]**self.S_D_resource_min)
				break
		for k in self.thresholds["A_resource_min"]:

			if self.A_resource_min <= k:
				self.S_A_resource_min = self.thresholds["A_resource_min"].index(k)
				self.stateID = self.stateID * (self.primes[3]**self.S_A_resource_min)
				break
		for k in self.thresholds["D_projectile_min"]:
			if self.D_projectile_min <= k:
				self.S_D_projectile_min = self.thresholds["D_projectile_min"].index(k)
				self.stateID = self.stateID * (self.primes[4]**self.S_D_projectile_min)
				break
		"""
		for k in self.thresholds["A_projectile_min"]:
			if self.A_projectile_min <= k:
				self.S_A_projectile_min = self.thresholds["A_projectile_min"].index(k)
				self.stateID = self.stateID * (self.primes[5]**self.S_A_projectile_min)
				break
		"""

		#debug 
		#print("State")
		#print(self.D_resource_min, self.S_D_resource_min)
		#print(self.A_resource_min, self.S_A_resource_min)
		

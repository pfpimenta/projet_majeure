#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# PROJET MAJEURE - Reinforcement Learning
# ERBACHER, Pierre
# FOLETTO PIMENTA, Pedro
# TIZON, Nicolas

import sys
from PyQt5.QtWidgets import QApplication, QWidget
PV_INITIAL = 3
DAMAGE = 1
RESOURCE_VALUE = 50
#team = 0 => ressource et block
#team = 1 => agent et tir (équipe bleu)
#team = 12 => agent et tir (équipe rouge)


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
			
	def draw(self):
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
		
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(400, 250)
    w.move(300, 300)
    w.setWindowTitle('REINFORCEMENT LEARNING')
    w.show()
    
    sys.exit(app.exec_())

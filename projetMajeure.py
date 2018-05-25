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

class Objet:
# classe pour tout les object qui sont dans l'environnement
	x = 0 # valeur par default
	y = 0
	dx = 0 # vitesses
	dy = 0
	def __init__(self,x=0,y=0, dx=0, dy=0):
		self.x = x;
		self.y = y;
		self.dx = dx;
		self.dy = dy;

	def move(self):
	# bouger l'agent d'accord avec sa vitesse
		self.x = self.x + self.dx;
		self.y = self.y + self.dy;

class Agent(Objet):
# classe pour les agents
	def __init__(self,x=0,y=0, dx=0, dy=0):
		Objet.__init__(self,x,y,dx,dy);
		self.pv = PV_INITIAL

	def shoot(self):
		pass  #TODO
		
	def action(self, state):
	# prendre une action
		pass # TODO

	def place_block(self):
	# placer un bloque en face du agent
		pass # TODO
	

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())

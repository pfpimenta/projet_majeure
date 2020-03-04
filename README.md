# PROJET MAJEURE - Reinforcement Learning

Code du projet de majeure a CPE Lyon
Ce projet met en place l'apprentissage de 2 équipes d'agents dans un environement (un jeu).
Ce projet à été réalisé dans le cardre du projet 'majeur' de spécialisation en fin de 4ème année à l'école de CPE Lyon.

Les auteurs:

* ERBACHER, Pierre
 
* FOLETTO PIMENTA, Pedro
 
* TIZON, Nicolas

![alt text](https://raw.githubusercontent.com/pfpimenta/projet_majeure/master/postermajeure.png)

Pour executer:

Pour charger des q-tables déjà existante :

python projetMajeure.py -l  

(l comme load => il faut que les tables porte le nom q_table_E1.npy et  q_table_E2.npy  et doivent être dans le même répertoire que projetMajeure.py)
 Il y a des tables que nous avons entraînés et sauvegardés dans le dossier 'Saves', il suffit de changer leur nom et de les sortir de ce dossier.


Pour entraîner et générer de nouvelles q-table :

python projetMajeure.py -t

Vous pouvez changez les paramètres d'entrainement dans l'entête du fichier projetMajeure.py ( ces paramètres commence par TRAINING)

TRAINING_N_EPISODE (: nombre de partie effectué)
TRAINING_N_STEP (: nombre d'action effectué par partie)
TRAINING_GAMMA 
TRAINING_LEARNING_RATE 

Pour modifier et expérimenter de nouvelle Recompenses, il faut modifier la fonction def calcul_reward
( et se servir des attributs des états : State.py)


A la fin de l'entrainement s'affiche dans la console dans l'ordre:
 - Le nombre de pommes ramassées par les bleus pour chaque episode
 - Le nombre de pommes ramassées par les rouges pour chaque episode 
 - Le nombre de victimes faites par les bleus pour chaque episode 
 - Le nombre de victimes faites par les rouges pour chaque episode 

Pour lancer la visualisation avec les nouvelles q-tables: 
python projetMajeure.py -l  




Faire un apprentissage par Q-Learning 'from scratch' (aucune bibliothèque d'apprentissage):
Le but de ce projet de creer son propre environement avec des règles simples puis d'entrainer un certain nombre d'agent par Q-Learning.

Création de l'environement:

Q-learning:
Qu'est ce que le Q-learning ? 
bla bla bla a compléter:

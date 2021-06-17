# Import de librairies python

import socket, sys, threading

##################################################
# Definition de classes							 #
##################################################

class Joueur1:

	def __init__(self):
		self.symbole = 'X'
		self.nbCoup = 0

	def demanderEntier(self):
		print("Entrez un entier :")
		colone = input()
		while( not colone.isnumeric()):
			print("La colone doit etre un entier :")
			colone = input()
		return int(colone)

	# Nom : choixColone
	# But : Demande au joueur 1 la colone a remplir et vérifie si l'entree est correcte et disponible au jeu
	# Entree : la grille, sa taille, le numero du joueur
	# Sortie : retourne la colone choisie par le joueur
	# verifie qu au moins une case est disponible dans la grille et que le numero correspond au range de la taille

	def choixColone(self, grille, size):
		valid = False
		print("Joueur 1 quelle colone ?")
		colone = self.demanderEntier()
		
		while not valid:
			if colone > 0 and colone <= size:
				if grille[0][colone - 1] == '.':
					valid = True
				else:
					print("Colone pleine, choisissez une autre colone")
					colone = self.demanderEntier()
			else:
				print("La colone doit être comprise entre 1 et ", size)
				colone = self.demanderEntier()
		return colone

	def envoyerMessage(self, message):
		print(message)

# Nom : Joueur2
# Class gestion du Joueur 2 par un thread pour maintenir la socket reseau
# comprend les fonctions necessaire pour interroger le joueur 2 et recuperer ses reponses
# Ainsi qu une fonction choixColone utilisant la socket

class Joueur2(threading.Thread):

	#dérivation d'un objet thread pour gerer la connexion avec joueur 2
	def __init__(self, conn):
		threading.Thread.__init__(self)
		self.connexion = conn
		self.nbCoup = 0
		self.symbole = 'O'
		
	def recevoirMessage(self):
		# reception message : soit FIN, soit un entier 
		msgJoueur2 = self.connexion.recv(1024).decode('utf-8').replace('\n','')
		if msgJoueur2.upper() == "FIN" or msgJoueur2 =="":
			self.shutdownSock()
		else:
			while ( not msgJoueur2.isnumeric() ):
				self.envoyerMessage("La colone doit etre un entier :")
				msgJoueur2 = self.connexion.recv(1024).decode('utf-8').replace('\n','')
			msgJoueur2 = int(msgJoueur2)
			return msgJoueur2  
	
	def envoyerMessage(self, message):
		message = message + '\n'
		self.connexion.send(message.encode())

	def shutdownSock(self):
		# Fermeture de la connexion :
		self.connexion.close()	  # couper la connexion cote serveur
		print("Joueur 2 déconnecté.")
		exit(0)
		# Le thread se termine ici 

	def choixColone(self, grille, size):
		valid = False
		self.envoyerMessage("Joueur 2 quelle colone ?")
		colone = self.recevoirMessage()
		while not valid:
			if colone > 0 and colone <= size:
				if grille[0][colone - 1] == '.':
					valid = True
				else:
					self.envoyerMessage("Colone pleine, choisissez une autre colone :")
					colone = self.recevoirMessage()
			else:
				self.envoyerMessage("La colone doit être comprise entre 1 et %s" % str(size))
				colone = self.recevoirMessage()
		return colone
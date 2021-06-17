# Import de librairies python

import socket, sys, threading, random

# Import de librairies personnelles

from classes import *
from fonctions import *

##################################################
# Definition de constantes 						 #
##################################################

HOST = '127.0.0.1'
PORT = 4444

# Taille de la grille, attention aux indices par la suite : de 0 a taille - 1 pour l indicage dans les tableaux
TAILLEGRILLE = 10

# nombre de pions a aligner pour gagner
NBPIONSVICTOIRE = 4


##################################################
# Fonction principale							 #
##################################################

def main():

	# initialisation du jeu soit nouvelle grille vide soit reprise fichier sauvegarde
	# joueur a commencer la partie, ou a reprendre celle en cours
	grille, fichierSauvegarde, numJoueur, nbTour = initialiserJeu(TAILLEGRILLE, "save.txt")

	# initialisation du joueur 1
	joueur1 = Joueur1()

	# Initialisation du serveur - Mise en place du socket :
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		mySocket.bind((HOST, PORT))
	except socket.error:
	 	print("La liaison avec le joueur 2 a echoue.")
	 	exit(0)
	print("Serveur pret, en attente du joueur 2")
	mySocket.listen(5)

	# Attente et prise en charge de la connexion du joueur 2 :
	connexion, adresse = mySocket.accept()

	# Créer un nouvel objet thread pour gérer la connexion / initialisation du joueur 2
	joueur2 = Joueur2(connexion)
	joueur2.start()
	envoyerMessage(joueur1, joueur2, "Joueur 2 connecte, adresse IP %s, port %s.\nLe jeu va commencer" % ( adresse[0], adresse[1]))
	joueur2.envoyerMessage("Vous etes le joueur 2")	

	# initialisation du jeu, envoi aux joueurs
	regles = affichJeu(NBPIONSVICTOIRE)
	envoyerMessage(joueur1, joueur2, regles)

	if numJoueur == 1: joueur1.envoyerMessage("Vous etes le joueur a jouer en premier :)")
	if numJoueur == 2: joueur2.envoyerMessage("Vous etes le joueur a jouer en premier :)")
	
	# affichage de la grille vide pour les deux joueurs
	grilleAafficher = affichGrille(grille, TAILLEGRILLE)
	envoyerMessage(joueur1, joueur2, grilleAafficher)

	# booleens de controle
	winner = False
	grillePleine = False

	while not winner and not grillePleine:
		nbTour += 1
		numJoueur = numJoueur % 2

		# message d attente pour l un et demande de saisie de l autre joueur
		if numJoueur == 1:
			joueur2.envoyerMessage("En attente d un mouvement du joueur 1")	
			colone = joueur1.choixColone(grille, TAILLEGRILLE) - 1   # Le joueur choisi une colone entre 1 et taille -> -1 pour revenir entre 0 et taille-1
			symbole = joueur1.symbole
		else:
			joueur1.envoyerMessage("En attente d un mouvement du joueur 2")
			colone = joueur2.choixColone(grille, TAILLEGRILLE) - 1
			symbole = joueur2.symbole

		fichierSauvegarde.write(str(symbole) + " " + str(colone) + "\n")

		grille, ligne = positionnerPion(grille, TAILLEGRILLE, colone, symbole)
		grilleAafficher = affichGrille(grille, TAILLEGRILLE)
		envoyerMessage(joueur1, joueur2, grilleAafficher)
		winner = testVictoire(grille, TAILLEGRILLE, ligne, colone, symbole, NBPIONSVICTOIRE)
		grillePleine = testGrillePleine(grille)

		numJoueur += 1

	final = Result(winner, joueur, nbTour + 1)
	joueur1.envoyerMessage(final)
	joueur2.envoyerMessage(final)
	joueur2.shutdownSock()
	fichierSauvegarde.close()
	exit(0)

if __name__ == "__main__":
	main()

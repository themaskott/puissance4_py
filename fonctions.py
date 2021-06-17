# Import de librairies python

import socket, sys, threading, random

##################################################
# Definition de fonctions						 #
##################################################


# Nom : initialiserJeu
# But : Affichage le menu du debut, permet de creer une partie ou de reprendre une partie sauvegardee
# Entree : taille de la grille pour l initialisation
# Sortie : une grille vide ou reconstituee de la derniere partie, le descripteur de fichier pour les sauvegardes, le joueur a jouer le prochain coup et le nb de tours
# Attention : pas de test sur l input()
# Amelioration : proposer le choix de la taille de la grille et du nb de pions a aligner
# Fichier : 1re ligne = taille de la grille / n lignes = 'symbole colone'

def initialiserJeu(size, nomFichier):
	menu = """
	Jeu de puissance 4
	Vous souhaitez : 
	1 - Une nouvelle partie
	2 - Reprendre la derniere partie
	3 - Quitter le jeu
	>>> """
	
	choix = int(input(menu))

	# creer un fichier vierge, une grille vide et les renvoyer
	if choix == 1:
		fichierSauvegarde = open(nomFichier,"w")
		fichierSauvegarde.write(str(size) + "\n")
		return iniGrille(size), fichierSauvegarde, random.randint(1,2), 0

	# reprendre le dernier fichier et le lire en completant une grille vierge de la bonne taille
	# le fermer et le renvoyer en mode append
	elif choix == 2:
		nbTour = 0
		fichierIn = open(nomFichier, "r")
		size = int(fichierIn.readline()) # premiere ligne = taille grille
		grille = iniGrille(size)

		line = fichierIn.readline()
		while line:
			nbTour += 1
			symbole, colone = line.split(' ')
			grille, l = positionnerPion(grille, size, int(colone), symbole)  # l ne sert a rien ici mais cf signature positionnerPion()
			line = fichierIn.readline()


		if symbole == 'X': prochainJoueur = 2
		else: prochainJoueur = 1

		fichierIn.close()
		fichierSauvegarde = open(nomFichier, "a")

		return grille, fichierSauvegarde, prochainJoueur, nbTour
	
	else:
		exit(0)



# Nom : affichJeu
# But : Affichage des regles du jeu
# Entree : neant
# Sortie : une chaine de caracteres = les regles du jeu a afficher

def affichJeu(size):
	message = """
	Jeu de puissance 4
	Joueur 1 joue avec les X
	Joueur 2 joue avec les O

	Le premier a aligner %d pions gagne :)

	""" % size
	return message


# Nom : iniGrille
# But : initialise un grille de jeu vide
# Entree : un entier n, taille de la grille
# Sortie : un tableau n x n rempli de "."

def iniGrille(size):
	grille = []
	for i in range(size):
		grille.append(['.'] * size)
	return grille

# Nom : affichGrille
# But : Affichage la grille
# Entree : nom de la grille et sa taille
# Sortie : une chaine de caracteres = la grille prete a son affichage
# Avec au dessus les numeros des colones

def affichGrille(grille, size):
	out = ""
	for ligne in grille:
		l = " ".join(ligne)
		out += l
		out += "\n"
	for i in range(size):
		out += str(i+1) + " "
	out += "\n"

	return out

# Nom : positionnerPion
# But : insere un pion dans la colone designee
# Entree : la grille, sa taille, la colone a remplir et le symbole du joueur
# Sortie : revoie une grille completee d un symbole et la ligne 0 a taille-1 pour le test a suivre (testVictoire)

def positionnerPion(grille, size, colone, symbole):
	l = 0
	while( grille[l][colone] == '.' ):
		if l == size - 1: break
		else: l += 1

	if l == size - 1 and grille[l][colone] == '.': 
		grille[l][colone] = symbole
		l = size
	else: 
		grille[l - 1][colone] = symbole
	
	return grille, l - 1


# Nom : testVictoire
# But : a partir des coordonnees du dernier pion insere, test les conditions de voctoire
# Entree : la grille, sa taille, ligne et colone du dernier pion, le symbole du joueur
# Sortie : revoie un booleen a True en cas de victoire


def testVictoire(grille, size, ligne, colone, symbole, nb):
	winner = False
	motifWinner = symbole * nb
	motifLigne = "".join(grille[ligne])
	motifColone = "".join(grille[l][colone] for l in range(size))

	# pour les diagonales on prend NBPIONSVICTOIRE de part et d autre du pion (ligne, colone)
	# diagonale 1 : x symboles en bas a droite + x symboles en haut a gauche
	motifDiag1 = symbole
	for i in range(1,nb):
		if (ligne + i < size) and (colone + i < size ):
			motifDiag1 = motifDiag1 + grille[ligne + i][colone + i]
	for i in range(1,nb):
		if (ligne - i > 0) and (colone - i > 0 ):
			motifDiag1 = grille[ligne - i][colone - i] + motifDiag1	

	# diagoanle 2 : x symboles en bas a gauche + x symboles en haut a droite
	motifDiag2 = symbole
	for i in range(1,nb):
		if (ligne - i > 0) and (colone + i < size ):
			motifDiag2 = motifDiag2 + grille[ligne - i][colone + i]
	for i in range(1,nb):
		if (ligne + i < size) and (colone - i > 0 ):
			motifDiag2 = grille[ligne + i][colone - i] + motifDiag2


	if motifWinner in motifColone or motifWinner in motifLigne or motifWinner in motifDiag1 or motifWinner in motifDiag2:
		winner = True

	return winner


def testGrillePleine(grille):
	return '.' not in grille[0]

# Nom : Result
# But : affiche le resultat de la partie
# Entree : joueur ayant potentiellement gagne, nb de coup joues
# Sortie : une chaine de caracteres a afficher correspandant au resultat de la partie
# Attention : toute la grille peut etre pleine et personne ne gagne

def Result(winner, joueur, nbTour):
	if nbTour % 2 == 0:
		nbCoupDuJoueur = nbTour // 2
	else:
		nbCoupDuJoueur = nbTour // 2 + 1
	if winner:
		return "Victoire du joueur " + str(joueur) + " en " + str(nbCoupDuJoueur) + " coups"
	else:
		return "Egalite, pas de vainqueur"


# Nom : envoyerMessage
# But : envoie le meme message aux deux joueurs
# Entree : les deux objets joueurs et le message a envoyer
# Sortie : neant

def envoyerMessage(joueur1, joueur2, message):
	joueur1.envoyerMessage(message)
	joueur2.envoyerMessage(message)

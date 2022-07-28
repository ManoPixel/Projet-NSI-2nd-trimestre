# Idées >
#Améliorer les vies > Batterie portable

#Fond d'écran
#Attaque
#Ennemis art
#Personnage art
#Boîte avec armes / fleche / chichote / bombe
#Diversité ennemis / rareté
#Farmer
#Boss
#Niveaux 
#Construction de base
#Potion de heal

import pyxel, random

dimension_ecran = 256
pyxel.init(dimension_ecran, dimension_ecran, title="Projet Tri2")
pyxel.load("design.3.pyxres", True, False, False, False)

#player[2] et player[3] sont les dimensions du joueur
#player[4] est la direction ou le tir part si le joueur appui le boutton
player = [dimension_ecran/2 - 8,dimension_ecran/2 - 8, 16,16, 2]

ennemis_liste = []
#types_ennemi[0] et [1] est le premier ennemi, dont la taille 8x8, puis [2] et [3] est un autre
types_ennemi = [15,11, 14,15, 14,16]

tir_taille = [4, 4, 32, 2]
tirs_liste = []
tir_selectionne = 0

vies = 10

commencer = 0 #Variable qui détermine quand le joueur est pret à joueur

score = 0
multiplicateur_score = 1

def choisir_difficulte():
    
    global commencer, multiplicateur_score
    
    
    if pyxel.btn(pyxel.KEY_1):
        difficulte_choisie = 1
        multiplicateur_score = difficulte_choisie
        commencer = 1
        return difficulte_choisie
    
    if pyxel.btn(pyxel.KEY_2):
        difficulte_choisie = 2
        multiplicateur_score = difficulte_choisie
        commencer = 1
        return difficulte_choisie
    
    if pyxel.btn(pyxel.KEY_3):
        difficulte_choisie = 3
        multiplicateur_score = difficulte_choisie
        commencer = 1
        return difficulte_choisie
    
    if pyxel.btn(pyxel.KEY_4):
        difficulte_choisie = 4
        commencer = 1
        return difficulte_choisie
    

def player_mouvement(x, y, tir_direction):
    """Mouvementation du joueur et le limite à rester dans l'écran
    Sous la forme player[x, y, taille_x, taille_y, tir_direction]
    Le mouvement du joueur change la direction du tir"""
    
    global dimension_ecran, player
    
    if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) :
        if x < dimension_ecran - player[2]:
            x = x + 2
            tir_direction = 2
    if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x = x - 2
            tir_direction = 4
    if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
        if y < dimension_ecran - player[3]:
            y = y + 2
            tir_direction = 3
    if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y = y - 2
            tir_direction = 1
            
    return x, y, tir_direction
    
    
def ennemis_creation(ennemis_liste):
    """Création des ennemis, l'ennemi est adicioné à la liste de ennemis, avec [x, y, taille_x, taille_y]"""
    global dimension_ecran, types_ennemi, vitesse_creation, difficulte_choisie
    
    if difficulte_choisie == 1:
        vitesse_creation = 30
        
    if difficulte_choisie == 2:
        vitesse_creation = 20
        
    if difficulte_choisie == 3:
        vitesse_creation = 15
        
    if difficulte_choisie == 4:
        vitesse_creation = 10
        
    
    if pyxel.frame_count % vitesse_creation == 0: #chaque seconde
        
        apparaitre_aleatoire = random.randint(1, 4) #determination aleatoire d'apparation d'ennemi
        ennemi_aleatoire = random.randint(0, len(types_ennemi)/2 - 1) #determination aleatoire de type d'ennemi
        taille = ennemi_aleatoire * 2
        
        if apparaitre_aleatoire == 1: #apparition en haut
            ennemi = [ random.randint(0, dimension_ecran), 0- types_ennemi[1 + taille] ]
            
        if apparaitre_aleatoire == 2: #apparition a droite
            ennemi = [ dimension_ecran + types_ennemi[0 + taille], random.randint(0, dimension_ecran) ]
            
        if apparaitre_aleatoire == 3: #apparition en bas
            ennemi = [ random.randint(0, dimension_ecran), dimension_ecran + types_ennemi[1 + taille] ]
            
        if apparaitre_aleatoire == 4: #apparition a gauche
            ennemi = [ 0, random.randint(0-types_ennemi[0 + taille], dimension_ecran) ]
            
        #Détermination aléatoire de taille d'ennemi par rapport à types_ennemi
        ennemi += types_ennemi[ 0 + taille], types_ennemi[1 + taille ]
        
        #Détermination de la vie
        vie_ennemi = ennemi_aleatoire + 1
        ennemi.append(vie_ennemi)
        
        #Détermination d'un sens pour tourner le sprite 
        ennemi.append(0)
        
        #Détermination aléatoire d'un sprite
        ennemi.append(random.randint(1,3))
        
        #Creation finale de l'ennemi
        ennemis_liste.append(ennemi)
        
    return ennemis_liste

def ennemis_mouvement(ennemis_liste):
    """Déplace les ennemis vers le centre du joueur"""
    
    global player
    
    for ennemi in ennemis_liste:
        
        if ennemi[0] < player[0] + player[2]/2 - ennemi[2]/2:
            ennemi[0] += 1
            
            #Ici l'ennemi regarde la droite
            ennemi[5] = 0

        if ennemi[0] > player[0] + player[2]/2 - ennemi[2]/2:
            ennemi[0] -= 1
            
            #Ici l'ennemi regarde la gauche
            ennemi[5] = 1
            
        if ennemi[1] < player[1] + player[3]/2 - ennemi[3]/2:         
            ennemi[1] += 1
            
        if ennemi[1] > player[1] + player[3]/2 - ennemi[3]/2:        
            ennemi[1] -= 1
                        
    return ennemis_liste 
    
def ennemis_colision(ennemis_liste):
    """Test si l'ennemi touche le joueur, si True, enlever une vie"""
    global vies
    
    for ennemi in ennemis_liste:
        if ( ennemi[0] <= player[0] + player[2] ) and\
           ( ennemi[1] <= player[1] + player[3] ) and\
           ( ennemi[0] + ennemi[2] >= player[0] )and\
           ( ennemi[1] + ennemi[3] >= player[1] ):
            
            #On enleve une vie par rapport à la vie de l'ennemi
            vies -= ennemi[4]
            #Vies étant devenu flottant doit être converti en entier
            #Pour un meillheur affichage
            vies = int(vies)
            
            ennemis_liste.remove(ennemi)
            
def tir_selection():
    """Le joueur appuye les nombres du clavier pour changer le type de tir qui sera tiré"""
    global tir_selectionne, multiplicateur_score, difficulte_choisie
    
    if pyxel.btnp(pyxel.KEY_1):
        tir_selectionne = 0
        multiplicateur_score = difficulte_choisie
        
    if pyxel.btnp(pyxel.KEY_2):
        tir_selectionne = 1
        multiplicateur_score = difficulte_choisie - 0.5
        
def tir_creation(tirs_liste, player):
    """Si le joueur appuye la touche espace, un tir est lancé
    Sous le format tir[x, y, taille_x, taille_y, tir_direction]"""
    global tir_taille, tir_selectionne, multiplicateur_score, difficulte_choisie
    
    tir_determine_x = tir_taille[tir_selectionne * 2]
    tir_determine_y = tir_taille[tir_selectionne * 2 + 1]
    
    milieu_x = player[2]/2 - tir_determine_x/2
    milieu_y = player[3]/2 - tir_determine_y/2
    
    
    
    if pyxel.btnp(pyxel.KEY_SPACE):
        
        if tir_selectionne == 0:
            multiplicateur_score = difficulte_choisie
            
        if tir_selectionne == 1:
            multiplicateur_score = difficulte_choisie - 0.5
            
        if player[4] == 1:
            tir = [player[0] + milieu_x , player[1] - tir_determine_y]
            
        if player[4] == 2:
            tir = [player[0] + player[2], player[1] + milieu_x]
            
        if player[4] == 3:
            tir = [player[0] + milieu_x, player[1] + player[3]]
            
        if player[4] == 4:
            tir = [player[0] - tir_determine_y , player[1] + milieu_x]
            
        #Ici le joueur regarde vers le haut ou vers le bas
        if player[4] == 1 or player[4] == 3:
            tir.append(tir_determine_x) #On adicionne à tir la taille_x
            tir.append(tir_determine_y) #On adicionne à tir la taille_y
            
        #Ici le joueur regarde vers la gauche ou droite
        #Alors on inverse la taille du tir 
        if player[4] == 2 or player[4] == 4:
            tir.append(tir_determine_y) #On adicionne à tir la taille_y
            tir.append(tir_determine_x) #On adicionne à tir la taille_x
        
        tir.append(player[4]) #On met la direction où part le tir
        
        tirs_liste.append(tir)
        
    return tirs_liste

def tir_mouvement(tirs_liste):
    """Bouge le tir jusqu'à la fin de l'ecran où aprés le passer, est exclu"""
    global dimension_ecran
    
    for tir in tirs_liste:
            
        if tir[4] == 1:
            if tir[1] + tir[3] > 0:
                tir[1] -= 3
            else:
                tirs_liste.remove(tir)
            
        if tir[4] == 2:
            if tir[0] - tir[2] < dimension_ecran:
                tir[0] += 3
            else:
                tirs_liste.remove(tir)
                
        if tir[4] == 3:
            if tir[1] - tir[2] < dimension_ecran:
                tir[1] += 3
            else:
                tirs_liste.remove(tir)
                
        if tir[4] == 4:
            if tir[0] + tir[2] > 0:
                tir[0] -= 3
            else:
                tirs_liste.remove(tir)
                
def tir_collision(ennemis_liste, tirs_liste):
    """Si le tir touche un ennemi, on enleve une vie de l'ennemi"""
    global tir_taille, multiplicateur_score, score
    
    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            if ( ennemi[0] <= tir[0] + tir[2] ) and\
               ( ennemi[1] <= tir[1] + tir[3] ) and\
               ( ennemi[0] + ennemi[2] >= tir[0] ) and\
               ( ennemi[1] + ennemi[3] >= tir[1] ):
                
                ennemi[4] -= 1 #enlever une vie de l'ennemi
                       
                score += ( 1 * multiplicateur_score) #score augmente
                
                if ennemi[4] == 0: #enlever ennemi mort
                    ennemis_liste.remove(ennemi)
                    
                tirs_liste.remove(tir)
                
####################################
def update():
    global player, ennemis_liste, commencer, difficulte_choisie, score
    
    if commencer == 0:
        difficulte_choisie = choisir_difficulte()
        
    elif vies > 0:
        
        player[0], player[1], player[4] = player_mouvement(player[0], player[1], player[4])
    
        ennemis_creation(ennemis_liste)
        ennemis_mouvement(ennemis_liste)
        ennemis_colision(ennemis_liste)
    
        tir_selection()
        tir_creation(tirs_liste, player)
        tir_mouvement(tirs_liste)
        tir_collision(ennemis_liste, tirs_liste)
        
    elif vies <= 0:            
        pyxel.quit()
        
        
####################################    

####################################
def draw():
    if commencer == 0:
        pyxel.cls(0)
        
        pyxel.rect(2, dimension_ecran/2 - 30, 60, 60, 11)
        pyxel.text(17, 124, "Easy (1)", 7)
            
        pyxel.rect(66, dimension_ecran/2 - 30, 60, 60, 10)
        pyxel.text(78, 124, "Medium (2)", 7)
            
        pyxel.rect(130, dimension_ecran/2 - 30, 60, 60, 9)
        pyxel.text(145, 124, "Hard (3)", 7)
            
        pyxel.rect(194, dimension_ecran/2 - 30, 60, 60, 8)
        pyxel.text(197, 124, "Impossible (4)", 7)
        
    elif vies > 0:
        
        #vide l'écran
        pyxel.cls(11)
        
        for ennemi in ennemis_liste: 
            #Dessiner les ennemis
                
            if ennemi[3] == 16: #Goblin
                #Tourner le sprite
                if ennemi [5] == 1:
                    largeur = -ennemi[2]
                else:
                    largeur = ennemi[2]
                
                #Différents goblins
                if ennemi[6] == 1:
                    x_pyxres, y_pyxres = 1, 32
                if ennemi[6] == 2:
                    x_pyxres, y_pyxres = 17, 32
                if ennemi[6] == 3:
                    x_pyxres, y_pyxres = 33, 32
                    
                pyxel.blt(ennemi[0], ennemi[1], 0, x_pyxres, y_pyxres, largeur, ennemi[3], 10)
                
            if ennemi[3] == 15: #Poule
                #Tourner le sprite
                if ennemi [5] == 1:
                    largeur = ennemi[2]
                else:
                    largeur = -ennemi[2]
                    
                #Différentes poules
                if ennemi[6] == 1:
                    x_pyxres, y_pyxres = 49, 33
                if ennemi[6] == 2:
                    x_pyxres, y_pyxres = 1, 49
                if ennemi[6] == 3:
                    x_pyxres, y_pyxres = 41, 113
                    
                pyxel.blt(ennemi[0], ennemi[1], 0, x_pyxres, y_pyxres, largeur, ennemi[3], 12)
            if ennemi[2] == 15: #Slime
                #Tourner le sprite
                if ennemi [5] == 1:
                    largeur = -ennemi[2]
                else:
                    largeur = ennemi[2]
                
                #Différents slimes
                if ennemi[6] == 1:
                    x_pyxres, y_pyxres = 0, 101
                if ennemi[6] == 2:
                    x_pyxres, y_pyxres = 0, 117
                if ennemi[6] == 3:
                    x_pyxres, y_pyxres = 16, 117
                    
                pyxel.blt(ennemi[0], ennemi[1], 0, x_pyxres, y_pyxres, largeur, ennemi[3], 7)
            
        for tir in tirs_liste:
           
            if tir[2] == 4:
                pyxel.blt(tir[0], tir[1], 0, 38, 86, tir[2], tir[3], 3)
            else:
                pyxel.rect(tir[0], tir[1], tir[2], tir[3], 12)
                
        #Dessiner le coeur
        if vies >= 10:
            pyxel.blt(0, 0, 0, 2, 4, 12, 12, 0)
        elif vies >= 8:
            pyxel.blt(0, 0, 0, 18, 4, 12, 12, 0)
        elif vies >= 6:
            pyxel.blt(0, 0, 0, 34, 4, 12, 12, 0)
        elif vies >= 4:
            pyxel.blt(0, 0, 0, 50, 4, 12, 12, 0)
        else:
            pyxel.blt(0, 0, 0, 2, 20, 12, 12, 0)
        if vies < 10:
            pyxel.text(4, 3, f"{vies}", 7)
        
        #Score
        pyxel.text(0, 15, f"Score: {score}", 7)
        
        pyxel.text(dimension_ecran -4, 0, f"{tir_selectionne}", 7)
        
        pyxel.rect(player[0], player[1], player[2], player[3], 7)
        
####################################

pyxel.run(update, draw)

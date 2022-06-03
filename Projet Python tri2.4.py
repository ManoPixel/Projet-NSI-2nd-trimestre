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

#player[2] et player[3] sont les dimensions du joueur
#player[4] est la direction ou le tir part si le joueur appui le boutton
player = [dimension_ecran/2 - 8,dimension_ecran/2 - 8, 16,16, 2]

ennemis_liste = []
#types_ennemi[0] et [1] est le premier ennemi, dont la taille 8x8, puis [2] et [3] est un autre
types_ennemi = [8,8, 10,10, 12,12]

tir_taille = [4, 4]
tirs_liste = []

vies = 10


def player_mouvement(x, y, tir_direction):
    """Mouvementation du joueur et le limite à rester dans l'écran"""
    
    global dimension_ecran, player
    
    if pyxel.btn(pyxel.KEY_D):
        if x < dimension_ecran - player[2]:
            x = x + 4
            tir_direction = 2
    if pyxel.btn(pyxel.KEY_A):
        if x > 0:
            x = x - 4
            tir_direction = 4
    if pyxel.btn(pyxel.KEY_S):
        if y < dimension_ecran - player[3]:
            y = y + 4
            tir_direction = 3
    if pyxel.btn(pyxel.KEY_W):
        if y > 0:
            y = y - 4
            tir_direction = 1
            
    return x, y, tir_direction
    
    
def ennemis_creation(ennemis_liste):
    """Création des ennemis, l'ennemi est adicioné à la liste de ennemis, avec [x, y, taille_x, taille_y]"""
    global dimension_ecran, types_ennemi
    
    if pyxel.frame_count % 30 == 0: #chaque seconde
        
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
        
        #Détermination de la vie de l'ennemi par rapport à sa taille
        vie_ennemi = types_ennemi[0 + taille] / 2 - 3
        ennemi.append(vie_ennemi)
        
        #Creation finale de l'ennemi
        ennemis_liste.append(ennemi)
        
    return ennemis_liste

def ennemis_mouvement(ennemis_liste):
    """Déplace les ennemis vers le centre du joueur"""
    
    global player
    
    for ennemi in ennemis_liste:
        
        if ennemi[0] < player[0] + player[2]/2 - ennemi[2]/2:
            ennemi[0] += 1

        if ennemi[0] > player[0] + player[2]/2 - ennemi[2]/2:
            ennemi[0] -= 1
                 
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
            
def tir_creation(tirs_liste, player):
    
    global tir_taille
    
    milieu_x = player[2]/2 - tir_taille[0]/2
    milieu_y = player[3]/2 - tir_taille[1]/2
    
    
    if pyxel.btnp(pyxel.KEY_SPACE):
        
        if player[4] == 1:
            tir = [player[0] + milieu_x , player[1] - tir_taille[1]]
            
        if player[4] == 2:
            tir = [player[0] + player[2], player[1] + milieu_y]
            
        if player[4] == 3:
            tir = [player[0] + milieu_x, player[1] + player[3]]
            
        if player[4] == 4:
            tir = [player[0] - tir_taille[0] , player[1] + milieu_y]
            
        tir.append(player[4])
        
        tirs_liste.append(tir)
        
    return tirs_liste

def tir_mouvement(tirs_liste):
    
    for tir in tirs_liste:
        
        if tir[2] == 1:
            tir[1] -= 3
            
        if tir[2] == 2:
            tir[0] += 3
            
        if tir[2] == 3:
            tir[1] += 3
            
        if tir[2] == 4:
            tir[0] -= 3
            
def tir_collision(ennemis_liste, tirs_liste):
    
    global tir_taille
    
    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            if ( ennemi[0] <= tir[0] + tir_taille[0] ) and\
               ( ennemi[1] <= tir[1] + tir_taille[1] ) and\
               ( ennemi[0] + ennemi[2] >= tir[0] ) and\
               ( ennemi[1] + ennemi[3] >= tir[1] ):
    
                ennemi[4] -= 1 #enlever une vie de l'ennemi
                           
                if ennemi[4] == 0: #enlever ennemi mort
                    ennemis_liste.remove(ennemi)
                    
                tirs_liste.remove(tir)
                
####################################
def update():
    global player, ennemis_liste
    
    player[0], player[1], player[4] = player_mouvement(player[0], player[1], player[4])
    
    ennemis_creation(ennemis_liste)
    ennemis_mouvement(ennemis_liste)
    ennemis_colision(ennemis_liste)
    
    tir_creation(tirs_liste, player)
    tir_mouvement(tirs_liste)
    tir_collision(ennemis_liste, tirs_liste)
####################################    

####################################
def draw():
    if vies > 0:
        
        #vide l'écran
        pyxel.cls(0)
            
        pyxel.text(0, 0, f"Vies: {vies}", 7)
    
        pyxel.rect(player[0], player[1], player[2], player[3], 7)
    
        for ennemi in ennemis_liste:
            if ennemi[4] == 3:
                couleur = 11
            if ennemi[4] == 2:
                couleur = 10
            if ennemi[4] == 1:
                couleur = 8
                
            pyxel.rect(ennemi[0], ennemi[1], ennemi[2], ennemi[3], couleur)
            
        for tir in tirs_liste:
            pyxel.rect(tir[0], tir[1], 4, 4, 2)
    
    elif vies <= 0:
        pyxel.quit()
        
####################################

pyxel.run(update, draw)

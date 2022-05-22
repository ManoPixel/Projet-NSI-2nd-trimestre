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

dimension_ecran = 512
pyxel.init(dimension_ecran, dimension_ecran, title="Projet Tri2")

#player[2] et player[3] sont les dimensions du joueur
player = [0, 0, 32, 32]

ennemis_liste = []

#types_ennemi[0] et [1] est le premier ennemi, dont la taille 8x8, puis [2] et [3] est un autre
types_ennemi = [8, 8, 16, 16, 10, 10]


vies = 10


def player_mouvement(x, y):
    """Mouvementation du joueur et le limite à rester dans l'écran"""
    
    global dimension_ecran, player
    
    if pyxel.btn(pyxel.KEY_D):
        if x < dimension_ecran - player[2]:
            x = x + 4
    if pyxel.btn(pyxel.KEY_A):
        if x > 0:
            x = x - 4
    if pyxel.btn(pyxel.KEY_S):
        if y < dimension_ecran - player[3]:
            y = y + 4
    if pyxel.btn(pyxel.KEY_W):
        if y > 0:
            y = y - 4
    return x, y
    
    
def ennemis_creation(ennemis_liste):
    """Création des ennemis, l'ennemi est adicioné à la liste de ennemis, avec [x, y, taille_x, taille_y]"""
    global dimension_ecran, types_ennemi
    
    if pyxel.frame_count % 30 == 0: #chaque seconde
        apparaitre_aleatoire = random.randint(1, 4) #determination aleatoire d'apparation d'ennemi
        ennemi_aleatoire = random.randint(0, len(types_ennemi)/2 - 1)
        
        if apparaitre_aleatoire == 1: #apparition en haut
            ennemis_liste.append([random.randint(0, dimension_ecran), 0- types_ennemi[1], types_ennemi[0 + (ennemi_aleatoire * 2)], types_ennemi[1 + (ennemi_aleatoire * 2)]])
            
        if apparaitre_aleatoire == 2: #apparition a droite
            ennemis_liste.append([dimension_ecran + types_ennemi[0], random.randint(0, dimension_ecran), types_ennemi[0 + ennemi_aleatoire * 2], types_ennemi[1 + ennemi_aleatoire * 2]])
            
        if apparaitre_aleatoire == 3: #apparition en bas
            ennemis_liste.append([random.randint(0, dimension_ecran), dimension_ecran + types_ennemi[1], types_ennemi[0 + ennemi_aleatoire * 2], types_ennemi[1 + ennemi_aleatoire * 2] ])
            
        if apparaitre_aleatoire == 4: #apparition a gauche
            ennemis_liste.append([0, random.randint(0-types_ennemi[0], dimension_ecran), types_ennemi[0 + ennemi_aleatoire * 2], types_ennemi[1 + ennemi_aleatoire * 2]])
        
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
        if ( ennemi[0] <= player[0] + player[2] ) and ( ennemi[1] <= player[1] + player[3] ) and ( ennemi[0] + ennemi[2] >= player[0] )and ( ennemi[1] + ennemi[3] >= player[1] ):
            vies -= 1
            ennemis_liste.remove(ennemi)
            
####################################
def update():
    global player, ennemis_liste
    
    player[0], player[1] = player_mouvement(player[0], player[1])
    
    ennemis_creation(ennemis_liste)
    ennemis_mouvement(ennemis_liste)
    ennemis_colision(ennemis_liste)
    
####################################    

####################################
def draw():
    if vies > 0:
        
        #vide l'écran
        pyxel.cls(0)
        
        pyxel.text(0, 0, f"Vies: {vies}", 7)
    
        pyxel.rect(player[0], player[1], player[2], player[3], 7)
    
        for ennemi in ennemis_liste:     
            pyxel.rect(ennemi[0], ennemi[1], ennemi[2], ennemi[3], 4)
    
    else:
        pyxel.quit()
        
####################################

pyxel.run(update, draw) 

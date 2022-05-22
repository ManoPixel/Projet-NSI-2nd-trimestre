import pyxel, random

#Améliorer les vies > Batterie portable
#Ennemis qui apparaissent aux coins
#

pyxel.init(1024, 1024, title="Projet Tri2")

player_x = 0
player_y = 0


ennemis_liste = []

vies = 100

def player_mouvement(x, y):
    if pyxel.btn(pyxel.KEY_D):
        if (x < 1016):
            x = x + 8
    if pyxel.btn(pyxel.KEY_A):
        if (x > 0):
            x = x - 8
    if pyxel.btn(pyxel.KEY_S):
        if (y < 992):
            y = y + 8
    if pyxel.btn(pyxel.KEY_W):
        if (y > 0):
            y = y - 8
    return x, y
    
def ennemis_creation(ennemis_liste):
    if pyxel.frame_count % 30 == 0:
        ennemis_liste.append([random.randint(0, 1024), random.randint(0, 1024)])
    return ennemis_liste

def ennemis_mouvement(ennemis_liste):
    
    global player_x, player_y
    for ennemi in ennemis_liste:
        
        if ennemi[0] < player_x:
            ennemi[0] += 1
        if ennemi[0] > player_x:
            ennemi[0] -= 1
                 
        if ennemi[1] < player_y:         
            ennemi[1] += 1
        if ennemi[1] > player_y:        
            ennemi[1] -= 1
            
#        if ennemi[0] == player_x and ennemi[1] == player_y:
#            ennemis_liste.remove(ennemi)
            
    return ennemis_liste 
    
def ennemis_colision(ennemis_liste):
    global vies
    for ennemi in ennemis_liste:
        if ennemi[0] <= player_x+8 and ennemi[1] <= player_y+32 and ennemi[0]+8 >= player_x and ennemi[1]+10 >= player_y:
            vies -= 1
            ennemis_liste.remove(ennemi)
            
####################################
def update():
    global player_x, player_y, ennemis_liste
    
    player_x, player_y = player_mouvement(player_x, player_y)
    
    ennemis_creation(ennemis_liste)
    ennemis_mouvement(ennemis_liste)
    ennemis_colision(ennemis_liste)
#####################################    
# fc paun osu
####################################
def draw():
    if vies > 0:
        
        #vide l'écran
        pyxel.cls(0)
        
        pyxel.text(0, 0, f"Vies: {vies}", 7)
    
        pyxel.rect(player_x, player_y, 8, 32, 7)
    
        for ennemi in ennemis_liste:     
            pyxel.rect(ennemi[0], ennemi[1], 8, 8, 4)
        
####################################
pyxel.run(update, draw) 
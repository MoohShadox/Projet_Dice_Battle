# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:49:25 2019

@author: PC MILO fixe
"""

import tkinter as tk
import numpy as np
import proba


N = 100
D = 20
dicesToLaunch = 1

tourJoueur = 1
autoRec = 0
autoRecTreshHold = 200

scores = np.zeros(2)
victoires = np.zeros(2)



"""
updateDicesToLaunch(n) :
affecte l'entier n à la valeur de dicesToLaunch (dés à lancer au prochain coup)
change aussi l'affichage pour correspondre à cette valeur
"""

def updateDicesToLaunch(n) :
    global dicesToLaunch
    dicesToLaunch = n
    launchDicesBtn.configure(text = "lancer " + str(dicesToLaunch) + " dés")
    
"""
updateScore() : appelée à chaque fois que le score change
permet d'afficher l'état du jeu au niveau des scores et nombre de victoires
reset aussi les scores et incrémente les victoires si l'un d'eux est supérieur à l'objectif
"""

def updateScore() :
    global scores
    global tourJoueur
    
    if(scores[0] >= N) :
        victoires[0] +=1
        reset()
    if(scores[1] >= N) :
        victoires[1] +=1
        reset()
    
    scoreJ1.configure(text= "J1 : " + str(scores[0]) + "   V : " + str(victoires[0]))
    scoreJ2.configure(text= "J2 : " + str(scores[1]) + "   V : " + str(victoires[1]))
    
    if tourJoueur == 1 :
        scoreJ1.configure(bg = "green")
        scoreJ2.configure(bg = "white")
    else :
        scoreJ1.configure(bg = "white")
        scoreJ2.configure(bg = "green")

"""
launchDices : lance autant de dés que la valeur de dicesToLaunch
"""

def launchDices() :
    global dicesToLaunch
    global tourJoueur
    global scores
    
    score = 0

    for i in range(dicesToLaunch) :
        dice = launchOneDice()
        if dice == 1 :
            score = 1
            break
        else :
            score += dice
            
    ##updateDicesToLaunch(1)
        
    if tourJoueur == 1 :
        scores[0] += score
        tourJoueur = 2
    else : 
        scores[1] += score
        tourJoueur = 1
    
    updateScore()
    
    automaticPlay()
    
"""
automaticPlay() : appelée à la fin d'un tour de jeu
si l'adversaire est dans un mode automatique, il joue immédiatemetn selon ce mode
"""
def automaticPlay() :
    global autoRec
    
    
    autoRec +=1
    
    if autoRec > autoRecTreshHold :
        autoRec = 0
    else :
        print("avant : " + str(tourJoueur))
        if tourJoueur == 2 and J2Mode.get() == 2 :
            updateDicesToLaunch(proba.coupOptimal(D, N, int(scores[1]), int(scores[0])))
            launchDices()
        if tourJoueur == 2 and J2Mode.get() == 3 :
            updateDicesToLaunch(proba.dStar(D))
            launchDices()
        if  tourJoueur == 2 and J2Mode.get() == 4 :
            updateDicesToLaunch(np.random.randint(1, 7))
            launchDices()
                
        if  tourJoueur == 1 and J1Mode.get() == 2 :
            updateDicesToLaunch(proba.coupOptimal(D, N, int(scores[0]), int(scores[1])))
            launchDices()
        if  tourJoueur == 1 and J1Mode.get() == 3 :
            updateDicesToLaunch(proba.dStar(D))
            launchDices()
        if  tourJoueur == 1 and J1Mode.get() == 4 :
            updateDicesToLaunch(np.random.randint(1, 7))
            launchDices()
        
"""
reset() :
methode qui remet les scores à zero (mais pas les victoires), donne le tour au joueur 1
"""
def reset() :
    global tourJoueur
    global scores
    
    tourJoueur = 1
    updateDicesToLaunch(1)
    scores = np.zeros(2)
    
    updateScore()

"""
launchOneDice() :
methode qui retourne un entier aléatoire entre 1 et 6
n'est pas différente de "np.random.randint(1,6)" en l'état, mais est utile pour la clarté et le debuggage
"""
def launchOneDice() :
    res = np.random.randint(1,6)
    return res
    

def moreDices() :
    global dicesToLaunch
    
    if dicesToLaunch < D :
        updateDicesToLaunch(dicesToLaunch+1)


def lessDices() :
    global dicesToLaunch
    
    if dicesToLaunch > 1 :
        updateDicesToLaunch(dicesToLaunch-1)
        
def applyBlindStrat() :
    
    updateDicesToLaunch(proba.dStar(D)) ## = min(D, 6)
    launchDices()
    
def applyRandStrat() :
    
    updateDicesToLaunch(np.random.randint(1, D+1)) ## = min(D, 6)
    launchDices()
    
def applyOptiStrat() :
    global scores
    
    if(tourJoueur == 1) :
        updateDicesToLaunch(proba.coupOptimal(D, N, int(scores[0]), int(scores[1])))
    else :
        updateDicesToLaunch(proba.coupOptimal(D, N, int(scores[1]), int(scores[0])))
    launchDices()
        
window = tk.Tk()
window.title("Dice Battle")

J1Mode = tk.IntVar()
J1Mode.set(1)
J2Mode = tk.IntVar()
J2Mode.set(1)

proba.initPdk(D, N + 6*D) 

launchDicesBtn = tk.Button(window, text = "lancer " + str(dicesToLaunch) + " dés", command = launchDices)
launchDicesBtn.grid(column=1, row=1)

lessDicesBtn = tk.Button(window, text = "-1", command = lessDices)
lessDicesBtn.grid(column=0, row=1)

moreDicesBtn = tk.Button(window, text = "+1", command = moreDices)
moreDicesBtn.grid(column=2, row=1)

resetBtn = tk.Button(window, text = "reset", command = reset)
resetBtn.grid(column=1, row=0)

applyBlindStratBtn = tk.Button(window, text = "appliquer la stratégie aveugle", command = applyBlindStrat)
applyBlindStratBtn.grid(column=3, row=1)

applyOptiStratBtn = tk.Button(window, text = "appliquer la stratégie optimale", command = applyOptiStrat)
applyOptiStratBtn.grid(column=3, row=3)

applyOptiStratBtn = tk.Button(window, text = "appliquer la stratégie aléatoire", command = applyRandStrat)
applyOptiStratBtn.grid(column=3, row=0)




tk.Label(window, 
        text=""" Mode J1 :""",
        justify = tk.LEFT,
        padx = 20).grid(column=0, row = 4)


tk.Radiobutton(window, 
              text="Joueur",
              padx = 20, 
              variable=J1Mode, 
              value=1).grid(column=0, row = 5)
tk.Radiobutton(window, 
              text="Optimal",
              padx = 20, 
              variable=J1Mode, 
              value=2).grid(column=0, row = 6)
tk.Radiobutton(window, 
              text="Aveugle",
              padx = 20, 
              variable=J1Mode, 
              value=3).grid(column=0, row = 7)
tk.Radiobutton(window, 
              text="Aléatoire",
              padx = 20, 
              variable=J1Mode, 
              value=4).grid(column=0, row = 8)


tk.Label(window, 
        text=""" Mode J2 :""",
        justify = tk.LEFT,
        padx = 20).grid(column=3, row = 4)
tk.Radiobutton(window, 
              text="Joueur",
              padx = 20, 
              variable=J2Mode, 
              value=1).grid(column=3, row = 5)
tk.Radiobutton(window, 
              text="Optimal",
              padx = 20, 
              variable=J2Mode, 
              value=2).grid(column=3, row = 6)
tk.Radiobutton(window, 
              text="Aveugle",
              padx = 20, 
              variable=J2Mode, 
              value=3).grid(column=3, row = 7)
tk.Radiobutton(window, 
              text="Aléatoire",
              padx = 20, 
              variable=J2Mode, 
              value=4).grid(column=3, row = 8)





scoreJ1 = tk.Label(window, text= "J1 : " + str(scores[0]) + "   V : " + str(victoires[0]), bg = "green")
scoreJ1.grid(column=0, row=0)
scoreJ2 = tk.Label(window, text= "J2 : " + str(scores[1]) + "   V : " + str(victoires[1]), bg = "white")
scoreJ2.grid(column=2, row=0)

automaticPlay()



window.mainloop()



N = 24
D = 10
tab = np.zeros((N,N))

proba.initPdk(D, N + 6*D)


for i in range(0, N) :
    for j in range(0, N) :
        tab[i, j] = proba.coupOptimal(D, N, i, j)
        
print(tab)



print(proba.coupOptimal(D, N, 1, 10))

## ayyaaa, ça marche
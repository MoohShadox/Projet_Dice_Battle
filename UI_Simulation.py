import numpy as np
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL

from Projet_MOGPL.opt_simultanee import distribution_probas, resolution_systemeD, remplir_strat, strat_ij, \
    optimization_sachantP2
from Projet_MOGPL.proba import dStar

D = 10
N = 100

#Calcule de la distribution mixte par défaut
dist = distribution_probas(D)
dist = np.array(dist)
dist_c = np.array(dist)
for i in range(0,len(dist)):
    dist_c[i] = dist[:i+1].sum()


def launchOneDice() :
    res = np.random.randint(1,6)
    return res


#Classe permettant la gestion et l'affichage d'un joueur
class Player_Layout():
    def __init__(self,number):
        self.mode = tk.StringVar()
        self.mode.set("Manuel")
        self.number = str(number)
        self.nb_dices = tk.IntVar()
        self.nb_dices.set(1)
        self.nb_points = tk.IntVar()
        self.nb_points.set(0)
        self.victoires = tk.IntVar()
        self.victoires.set(0)


    def getPane(self,root):
        p = tk.PanedWindow(root, orient=VERTICAL)
        p.add(tk.Label(p,text="Joueur : " + self.number))
        p.add(tk.Radiobutton(p,text = "Automatique",variable = self.mode,value = "Automatique"))
        p.add(tk.Radiobutton(p,text ="Manuel",variable = self.mode, value = "Manuel"))


        points_layout =  tk.PanedWindow(p, orient=HORIZONTAL)
        p.add(points_layout)
        points_layout.add(tk.Label(points_layout, text="Des a jouer : "))
        points_layout.add(tk.Entry(points_layout,textvariable=self.nb_dices,width=5))

        points_layout = tk.PanedWindow(p, orient=HORIZONTAL)
        p.add(points_layout)
        points_layout.add(tk.Label(points_layout, text="Victoires : "))
        points_layout.add(tk.Label(points_layout, textvariable=self.victoires))

        points_layout = tk.PanedWindow(p, orient=HORIZONTAL)
        p.add(points_layout)
        points_layout.add(tk.Label(points_layout, text="Points : "))
        points_layout.add(tk.Label(points_layout, textvariable=self.nb_points))

        return p





    def jeterDes(self,nb):
        points = 0
        print("Mode = ",self.mode.get())
        print("nombre nb = ",nb," par le joueur ",self.number)
        for i in range(0, nb):
            d = launchOneDice()
            points = points + d
            if (d == 1):
                points = 1
                break
        return points

    def calculerJet(self,dist_w=dist_c):
        print("Mode de ",self.number," : ",self.mode.get())
        if(self.mode.get() == "Manuel"):
            return self.calculerJetManuel()
        print("Le joueur ",self.number," joue suivant la distribution : ",dist_w)
        return self.calculerJetAutomatique(dist_w=dist_w)


    def calculerJetManuel(self):
        return self.jeterDes(self.nb_dices.get())


    def calculerJetAutomatique(self,dist_w = dist_c):
        r = np.random.rand()
        d = 0
        print("r = ",r)
        print("distribution utilisée par le jet automatique ; ", dist_w)
        for i in range(0, len(dist_w)):
            if (r <= dist_w[i]):
                d = i+1
                break
        if(self.mode.get()== "Automatique"):
            self.nb_dices.set(d)
        print("Nombre de dés aprés calcul : ",d)
        return self.jeterDes(d)

    def getPoints(self):
        return self.nb_points.get()

    def resetPoints(self):
        self.nb_points.set(0)

    def setPoints(self,points):
        self.nb_points.set(points)
        if(self.nb_points.get()>=N):
            self.nb_points.set(0)
            self.victoires.set(self.victoires.get()+1)






import numpy as np

window = tk.Tk()

J1 = Player_Layout(1)
J2 = Player_Layout(2)

#Scénarion 01 : Tour classique
def jouer_tour(dist_w=dist_c):
    global J1
    global J2
    print("--------Début------------")
    jet1, jet2 = J1.calculerJet(dist_w) , J2.calculerJet(dist_w)
    P1 = jet1 + J1.getPoints()
    P2 = jet2 + J2.getPoints()
    print("Le joueur 1 fait : ",jet1)
    print("Le joueur 2 fait ",jet2)
    if(P1 < N and P2 < N):
        J1.setPoints(P1)
        J2.setPoints(P2)
    elif(P1 < N or P2>P1):
        J2.setPoints(P2)
        J1.resetPoints()
    elif(P2 < N or P1>P2):
        J1.setPoints(P1)
        J2.resetPoints()
    print("--------Fin------------")

#Scénario 2 : Tour simplifié
def jouer_tour_un_coup(dist_w=dist_c):
    global J1
    global J2
    print("--------Début------------")
    P1 = J1.calculerJet(dist_w)
    P2 = J2.calculerJet(dist_w)
    if(P1>P2):
        J1.victoires.set(J1.victoires.get()+1)
    elif(P1<P2):
        J2.victoires.set(J2.victoires.get() + 1)
    print("--------Fin------------")


#Fonctions servant a effectuer des simulations


def construire_simulation(dist_c):
    global step
    s = int(step.get())
    m1 = J1.mode.get()
    m2 = J2.mode.get()
    J1.mode.set("Manuel")
    J1.nb_dices.set(5)
    print("DStar a donné  :", dStar(D))
    J2.mode.set("Automatique")
    for i in range(0,s):
        jouer_tour(dist_w= dist_c)
    J1.mode.set(m1)
    J2.mode.set(m2)
    ratio = J2.victoires.get() / (J1.victoires.get() + J2.victoires.get()) * 100
    return ratio

def simuler_tour(dist_c):
    #J1.mode.set("Manuel")
    #J1.nb_dices.set(dStar(10))
    #J2.mode.set("Automatique")
    #jouer_tour(dist_c)
    J2.mode.set("Automatique")
    #J1.nb_dices.set(dStar(10))
    J1.mode.set("Manuel")
    J1.nb_dices.set(dStar(D))
    jouer_tour(dist_c)


def simulation_facultative():
    global N
    global D
    remplir_strat(N,D)
    print(strat_ij)
    s = {}
    for i in strat_ij:
        s[str(i)] = strat_ij[i]
    import json
    with open('result.json', 'w') as fp:
        json.dump(s, fp)
    pass

def simulation_fichier():
    import json
    global strat_ij
    global D
    global N
    import pandas as pd
    global step
    strat_ij.clear()
    r = open("result.json")
    strat = json.loads(r.read())
    strat_ij = {}
    for i in strat:
        t = tuple(i.replace(",","").replace("(","").replace(")","").split(" "))
        t2 = []
        for j in t:
            t2.append(int(j))
        t2 = tuple(t2)
        strat_ij[t2] = strat[i]

    step.set(100000)
    s = 10000000
    L = {}
    for j in range(0,1000):
        dist_lue = strat_ij[(J2.nb_points.get(),J1.nb_points.get())]
        print("distribution lue = ",dist_lue)
        print("Nombre de dés", D)
        dist_lue = np.array(dist_lue)
        dist_r = np.array(dist_lue)
        for j in range(0, len(dist_lue)):
            dist_r[j] = dist_lue[:j + 1].sum()
        simuler_tour(dist_r)
    L["Nombre de dés"] = L.get("Nombre de dés", []) + [D]
    L["Pourcentage de Victoires"] = L.get("Pourcentage de Victoires", []) + [J2.victoires.get()/(J1.victoires.get()+J2.victoires.get())*100]
    J1.victoires.set(0)
    J2.victoires.set(0)
    df = pd.DataFrame(L)
    f = open("experimentation3.html", "w")
    f.write(df.to_html())
    print(df)

def correctif_simulation():
    global N
    global D
    distribution_tirage = resolution_systemeD(D)
    #distribution_tirage = np.array([0, 0.17, 0.05, 0.78, 0 , 0 , 0 , 0])
    #[0.25104022 0.32316227 0.32316227 1.         1.         1.
        #1.         1.         1.         1.        ]
    distribution_tirage = distribution_tirage[1:]
    distribution_cumule = np.array(distribution_tirage)
    print('distribution tirage = ',distribution_tirage)
    for i in range(0,len(distribution_tirage)):
        distribution_cumule[i] = np.array(distribution_tirage[:i+1]).sum()
    print("Distribution cumulee = ",distribution_cumule)
    J1.victoires.set(0)
    J2.victoires.set(0)
    J1.mode.set("Manuel")
    J2.mode.set("Manuel")
    J2.nb_dices.set(6)
    for i in range(0,10000):
        print("iteration : ",i)
        r = np.random.rand()
        d = 0
        for i in range(0,len(distribution_cumule)):
            d=0
            if(r<=distribution_cumule[i]):
                d= i+1
                break
        #print(optimization_sachantP2( np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),D))
        #J1.nb_dices.set(optimization_sachantP2(D,[0,0,0,0,0,1,0,0,0,0]))
        J1.nb_dices.set(d)
        jouer_tour_un_coup()
    print("Nombre de victoires de 1 : ",J1.victoires.get())
    print("Nombre de victoires de 2 : ",J2.victoires.get())
    print("Pourcentage de victoire : ", J1.victoires.get() / (J1.victoires.get() + J2.victoires.get()) * 100)


def correctif_simulation_fichier():
    global N
    global D
    import json
    strat_ij = {}
    r = open("result.json")
    strat = json.loads(r.read())
    strat_ij = {}
    for i in strat:
        t = tuple(i.replace(",", "").replace("(", "").replace(")", "").split(" "))
        t2 = []
        for j in t:
            t2.append(int(j))
        t2 = tuple(t2)
        strat_ij[t2] = strat[i]
    J1.victoires.set(0)
    J2.victoires.set(0)
    J1.mode.set("Manuel")
    J2.mode.set("Manuel")
    J2.nb_dices.set(6)
    cpt = 0
    stats = []
    for x in range(0,50):
        for k in range(0, 1000):
            print("iteration : ", k)
            print("Nombre de points : i=",J1.nb_points.get()," j=",J2.nb_points.get())
            distribution_tirage = strat_ij[(J1.nb_points.get(),J2.nb_points.get())]
            # distribution_tirage = np.array([0, 0.17, 0.05, 0.78, 0 , 0 , 0 , 0])
            # [0.25104022 0.32316227 0.32316227 1.         1.         1.
            # 1.         1.         1.         1.        ]
            distribution_cumule = np.array(distribution_tirage)
            print('distribution tirage = ', distribution_tirage)
            for i in range(0, len(distribution_tirage)):
                distribution_cumule[i] = np.array(distribution_tirage[:i + 1]).sum()
            print("Distribution cumulee = ", distribution_cumule)
            r = np.random.rand()
            d = 0
            for i in range(0, len(distribution_cumule)):
                d = 0
                if (r <= distribution_cumule[i]):
                    d = i + 1
                    break
            # print(optimization_sachantP2( np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),D))
            # J1.nb_dices.set(optimization_sachantP2(D,[0,0,0,0,0,1,0,0,0,0]))
            J1.nb_dices.set(d)
            if(d==6):
                cpt = cpt +1
            jouer_tour()
            print("Nombre de victoires de 1 : ", J1.victoires.get())
            print("Nombre de victoires de 2 : ", J2.victoires.get())
        stats.append(J1.victoires.get() / (J1.victoires.get()+J2.victoires.get())*100)
        J1.victoires.set(0)
        J2.victoires.set(0)
    print(cpt/10000)
    stats = np.array(stats)
    print("Pourcentage de victoire : ",stats)
    print("Moyenne : ",stats.mean())
    print("Ecart type : ",stats.std())



def construire_fichier_simulation():
    global D
    global N
    import pandas as pd
    global step
    tmp = D
    tmp2 = step.get()
    step.set(10000)
    L = {}
    for i in range(5,7):
        dist = resolution_systemeD(D)[1:]
        print("Aprés résolution la distribution est : ",dist)
        print("distribution : ",dist)
        print("Nombre de dés",D)
        dist = np.array(dist)
        dist_r = np.array(dist)
        for j in range(0, len(dist)):
            dist_r[j] = dist[:j + 1].sum()
        L["Nombre de dés"] = L.get("Nombre de dés",[]) + [i]
        L["Pourcentage de Victoires"] = L.get("Pourcentage de Victoires", []) + [construire_simulation(dist_r)]
    df = pd.DataFrame(L)
    f = open("experimentation2.html","w")
    f.write(df.to_html())
    print(df)

def optimal1vsOptimal2():
    global N
    global D
    import json
    strat_ij = {}
    distribution_tirage = resolution_systemeD(D)
    # distribution_tirage = np.array([0, 0.17, 0.05, 0.78, 0 , 0 , 0 , 0])
    # [0.25104022 0.32316227 0.32316227 1.         1.         1.
    # 1.         1.         1.         1.        ]
    distribution_tirage = distribution_tirage[1:]
    distribution_cumule1 = np.array(distribution_tirage)
    print('distribution tirage = ', distribution_tirage)
    for i in range(0, len(distribution_tirage)):
        distribution_cumule1[i] = np.array(distribution_tirage[:i + 1]).sum()
    r = open("result.json")
    strat = json.loads(r.read())
    strat_ij = {}
    for i in strat:
        t = tuple(i.replace(",", "").replace("(", "").replace(")", "").split(" "))
        t2 = []
        for j in t:
            t2.append(int(j))
        t2 = tuple(t2)
        strat_ij[t2] = strat[i]
    J1.victoires.set(0)
    J2.victoires.set(0)
    J1.mode.set("Manuel")
    J2.mode.set("Manuel")
    J2.nb_dices.set(6)
    cpt = 0
    stats = []
    for x in range(0,50):
        for k in range(0, 1000):
            print("iteration : ", k)
            print("Nombre de points : i=",J1.nb_points.get()," j=",J2.nb_points.get())
            distribution_tirage = strat_ij[(J1.nb_points.get(),J2.nb_points.get())]
            # distribution_tirage = np.array([0, 0.17, 0.05, 0.78, 0 , 0 , 0 , 0])
            # [0.25104022 0.32316227 0.32316227 1.         1.         1.
            # 1.         1.         1.         1.        ]
            distribution_cumule = np.array(distribution_tirage)
            print('distribution tirage = ', distribution_tirage)
            for i in range(0, len(distribution_tirage)):
                distribution_cumule[i] = np.array(distribution_tirage[:i + 1]).sum()
            print("Distribution cumulee = ", distribution_cumule)
            r = np.random.rand()
            d = 0
            for i in range(0, len(distribution_cumule)):
                d = 0
                if (r <= distribution_cumule[i]):
                    d = i + 1
                    break
            # print(optimization_sachantP2( np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),D))
            # J1.nb_dices.set(optimization_sachantP2(D,[0,0,0,0,0,1,0,0,0,0]))
            J1.nb_dices.set(d)
            r = np.random.rand()
            d = 0
            for i in range(0, len(distribution_cumule1)):
                d = 0
                if (r <= distribution_cumule1[i]):
                    d = i + 1
                    break
            J2.nb_dices.set(d)
            jouer_tour()
            print("Nombre de victoires de 1 : ", J1.victoires.get())
            print("Nombre de victoires de 2 : ", J2.victoires.get())
        stats.append(J1.victoires.get() / (J1.victoires.get()+J2.victoires.get())*100)
        J1.victoires.set(0)
        J2.victoires.set(0)
    print(cpt/10000)
    stats = np.array(stats)
    print("Pourcentage de victoire : ",stats)
    print("Moyenne : ",stats.mean())
    print("Ecart type : ",stats.std())


step = tk.StringVar()

P1 = J1.getPane(window)
P2 = J2.getPane(window)

P1.grid(column = 0,row = 0)
P2.grid(column = 2,row = 0)

tk.Button(window,text="Lancer",command=jouer_tour).grid(column = 1,row = 0)
tk.Entry(window,textvariable=step).grid(column = 1,row = 2)
simulations_layout =  tk.PanedWindow(window, orient=HORIZONTAL)
simulations_layout.grid(column = 1,row = 3)
#simulations_layout.add(tk.Button(simulations_layout,text="Simuler",command=simulation_facultative))
#simulations_layout.add(tk.Button(simulations_layout,text="Simuler",command=simulation_fichier))
simulations_layout.add(tk.Button(simulations_layout,text="Aveugle vs Optimal Aveugle",command=correctif_simulation))
simulations_layout.add(tk.Button(simulations_layout,text="Calculer Stratégie Optimale",command=simulation_facultative))
simulations_layout =  tk.PanedWindow(window, orient=HORIZONTAL)
simulations_layout.grid(column = 1,row = 4)
simulations_layout.add(tk.Button(simulations_layout,text="Aveugle vs Optimal ",command=correctif_simulation_fichier))
simulations_layout.add(tk.Button(simulations_layout,text="Optimal Aveugle vs Optimal",command=optimal1vsOptimal2))
window.title("Dice Battle Version Simultanée")

import matplotlib.pyplot as plt

window.mainloop()

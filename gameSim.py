from Projet_MOGPL.proba import calculPdk
import pandas as pd

import numpy as np

max_D = 10
max_P = 100

#Calcul une seule fois des probabilités nécessaires au calcul
def affichage_probas_points(d):
    P = calculPdk(d,6*d)
    D = pd.DataFrame(P)
    print(D)
    f = open("table.html","w")
    f.write(D.to_html())
    print(P.sum(axis=1))




def esperance_d1_d2(d1,d2,joueur = 1):
    #Calcul de toutes les jointes
    P1 = calculPdk(d1,6*d1)
    P2 = calculPdk(d2,6*d2)
    #Probabilité que d2 fasse un score de 1 et pas d1
    Pn11 = P2[d2,1] * (1-P1[d1,1])
    P1n1 = P1[d1,1] * (1-P2[d2,1])
    P11 = P1[d1,1] * P2[d2,1]
    sum_V = 0
    sum_D = 0
    sum_N = 0
    #Calcule de la somme des probabilités des issues de victoire pour le joueur, de défaite et de match nul
    for j in range(2*d1,6*d1):
        for k in range(2*d2,6*d2):
            if(j>k):
                sum_V = sum_V + P1[d1][j] * P2[d2][k]
            elif(j<k):
                sum_D = sum_D + P1[d1][j] * P2[d2][k]
            else:
                sum_N = sum_N + P1[d1][j] * P2[d2][k]
    sum_V = sum_V + Pn11
    sum_D = sum_D + P1n1
    sum_N = sum_N + P11
    if(joueur == 1):
        return sum_V - sum_D
    else:
        return sum_D - sum_V

def esperance_d1_d2(d1,d2,joueur = 1):
    P = calculPdk(max(d1,d2),6*max(d1,d2))
    sum_V = 0
    sum_D = 0
    sum_N = 0
    for j in range(1,6*d1+1):
        for k in range(1,6*d2+1):
            if(j>k):
                #print("Victoire j=",j," k=",k)
                #print("On ajoute ",P[d1,j]," * ",P[d2,k]," = ",P[d1,j]*P[d2,k])
                sum_V = sum_V + P[d1,j]*P[d2,k]
            elif (j < k):
                #print("Defaite j=", j, " k=", k)
                #print("On soustrait ", P[d1, j], " * ", P[d2, k], " = ", P[d1, j] * P[d2, k])
                sum_D = sum_D + P[d1,j] * P[d2,k]
            else:
                sum_N = sum_N + P[d1,j] * P[d2,k]

    if (joueur == 1):
        return sum_V - sum_D
    else:
        return sum_D - sum_V

def generation_matrice(D):
    Arr = np.zeros((D+1,D+1))
    for i in range(1,D+1):
        for j in range(1,D+1):
            Arr[i][j] = esperance_d1_d2(i,j,joueur=1)
    D = pd.DataFrame(Arr)
    f = open("matrice_esperance.html", "w")
    f.write(D.to_html())
    return Arr


from gurobipy import *
esperance_d1_d2(1,6)
generation_matrice(10)
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 12:42:00 2019

@author: PC MILO fixe
"""
import numpy as np


memoQ = {}
memoEG = {}
memoCO = {}

"""
d integer :
k integer :
return float : probabilité d'obtenir k points en jetant d dés sachant qu'aucun 
ne tombe sur 0
"""
def Q(d, k) :
    
    if (d, k) in memoQ :
        return memoQ[(d, k)]
    
    if k <= 1 :
        return 0
    
    if d == 1 and (2 <= k and k <= 6) :
        return 1/5
    if d >= 2 and (2*d <= k and k <= 6*d) :
        val = (Q(d-1, k-2) + Q(d-1, k-3) + Q(d-1, k-4) + Q(d-1, k-5) + Q(d-1, k-6))/5
        memoQ[(d, k)] = val
        return val
    
    return 0


"""
calculPdk(dMax, kMax) :
dMax integer : le nombre maximal de dés lançables
kMax integer : l'objectif de score à atteindre
return ndarray :
renvoie la matrice des chances d'avoir k en lançant d dés pour k de 1 à kMax 
et de d à dMax
"""
def calculPdk(dMax, kMax) :
    Pdk = np.zeros((dMax+1, kMax+1))
    
    Pdk[0, 0] = 1
    
    for d in range(1, dMax+1) :
        for k in range(1, kMax+1) :
            
            if k == 1 :
                Pdk[d, k] = 1 - pow((5/6), d)
            if (2 <= k and k<=2*d-1) or 6*d < k :
                Pdk[d, k] = 0
            if 2*d <= k and k<=6*d :
                Pdk[d, k] = pow((5/6), d) * Q(d, k)
    return Pdk

"""
initPdk(D, N) :
D integer : le nombre maximal de dés lançables
N integer : l'objectif de score à atteindre
Lance le calcul de Pdk à l'aide de calculPdk et le stocke dans la variable 
globale Pdk.
Utile pour initialiser Pdk depuis un autre script.
"""
def initPdk(D, N) :
    global Pdk
    
    Pdk = calculPdk(D, N)

"""
EGOpti(D, N, i, j) :
D integer : le nombre maximal de dés lançables
N integer : l'objectif de score à atteindre
i integer : le score du joueur dont on calcule l'espérance
j integer : le score du joueur dont on ne calcule pas l'espérance
return float :
Calcule l'espérance de gain d'un joueur dans le cas où il a un score de i, 
son adversaire a j et le jeu a pour paramètres N et D et où les deux joueurs 
jouent de manière optimale.
"""

def EGOpti(D, N, i, j) :
    global Pdk
    
    if(i >= N):
        return 1
    if(j >= N):
        return 0
    if (D, N, i, j) in memoEG :
        return memoEG[(D, N, i, j)]
    d = coupOptimal(D, N, i, j)
    val1 = 0
    for k in range (N-i, N + 6*D) :
        val1 += Pdk[d, k]
    val2 = 0
    for k in range(1, N-i-1) :
        val2 += Pdk[d, k]*EGOpti(D, N, j, i+k)
    memoEG[(D, N, i, j)] = val1-val2
    return val1 - val2
    


"""
coupOptimal(D, N, i, j) :
D integer : le nombre maximal de dés lançables
N integer : l'objectif de score à atteindre
i integer : le score du joueur dont on calcule le coup optimal
j integer : le score du joueur dont on ne calcule pas le coup optimal
return integer : le nombre de dés à lancer
Calcule le nombre de dés qu'un joueur doit lancer dans le cas où il a un score 
de i, son adversaire a j et le jeu a pour paramètres N et D et où les deux 
joueurs jouent de manière optimale.
"""
def coupOptimal(D, N, i, j) :
    global Pdk
    
    if (D, N, i, j) in memoCO :
        return memoCO[(D, N, i, j)]
    val = 0
    valMax = -1
    dOpti = 0
    
    for d in range(1, D+1) :
        val = 0
        val1 = 0
        for k in range(N-i, N+6*D) :
            val1 += Pdk[d, k]
        val2 = 0
        for k in range(1, N-i-1) :
            val2 += Pdk[d, k]*EGOpti(D, N, j, i+k)
        val = val1-val2
        if val > valMax :
            valMax = val
            dOpti = d
       
    memoCO[(D, N, i, j)] = dOpti   
    return dOpti

"""
d integer : nombre de dés à lancer
return float : l'espérance des score obtenu par le lancer de d dés
"""
def EP(d) :
    return 4*d*pow((5/6), d) + 1 - pow((5/6), d)

"""
D integer : nombre de dés à lancer maximal
return integer : le nombre de dés dont l'espérance est la plus haute
"""
def dStar(D) :
    eMax = 0
    dMax = 0
    for d in range(1, D+1) :
        ep = EP(d)
        if(ep > eMax) :
            eMax = ep
            dMax = d
    return dMax






    
"""

PARTIE GENERALE

"""

memoMDGE = {}
memoE1 = {}

"""
D integer : le nombre maximal de dés lançables
N integer : l'objectif de score à atteindre
i integer : le score du joueur 1
j integer : le score du joueur 2
EG ndarray : tableau contenant les valeurs EG(k, l) avec k > i et l > j
return ndarray : la matrices des gains E1(i, j)
"""
def matriceDesGainsE1(D, N, i, j, EG) :
    
    if i >= N or j >= N :
        if i > j :
            return np.ones((D+1, D+1))
        if j > i :
            return np.zero((D+1, D+1))
        if i ==j :
            return -np.ones((D+1, D+1))
            
    
    if (D, N, i, j) in memoMDGE :
        return memoMDGE[(D, N, i, j)]
    
    res = np.zero((D+1, D+1))
    
    for a in range(1,D+1) :
        for b in range(1,D+1) :
            res[a, b] = E1(D, N, a, b, i, j, EG)
            
    memoMDGE[(D, N, i, j)] = res
    
    return res


"""
D integer : le nombre maximal de dés lançables
N integer : l'objectif de score à atteindre
d1 integer : le nombre de dés lancés par le joueur 1
d2 integer : le nombre de dés lancés par le joueur 2
i integer : le score du joueur 1
j integer : le score du joueur 2
EG ndarray : tableau contenant les valeurs EG(k, l) avec k > i et l > j
return float : l'espérance de gain du joueur 1 dans le cas ou il lance d1 dés 
et son aversaire d2 dés et que l'on est en l'état i, j
"""
def E1(D, N, d1, d2, i, j, EG) :
    
    
    if (D, N, d1, d2, i, j) in memoE1 :
        return memoE1[(D, N, d1, d2, i, j)]
    
    sum1 = 0
    
    for k in range(N-i, N+6*D) :
        for l in range(1, k) :
            sum1 = sum1 + Pdk[d1, k]*Pdk[d2, l]
    sum2 = 0
    
    for k in range(N-j, N+6*D) :
        for l in range(1, k) :
            sum2 = sum2 + Pdk[d1, l]*Pdk[d2, k]
    
    sum3 = 0
    
    for k in range(1, N-i) :
        for l in range(1, N-j) :
            sum3 = sum3 + Pdk[d1, k]*Pdk[d2, l] * EG[i+k, j+l]
            
    val = sum1 - sum2 + sum3
    memoE1[(D, N, d1, d2, i, j)] = val
    
    return val

def init_EG(N,D):
    EG = np.zeros((N+6*D,N+6*D))
    initPdk(D, N + 6 * D)
    for i in range(N-1,N+6*D):
        for a in range(0, N-1):
            EG[i,a] = 1
            EG[a, i] = -1
    for i in range(N-1,N+6*D):
        for j in range(N-1,N+6*D):
            if(i>j):
                EG[i,j] = 1
                EG[j,i] = -1
            elif(j>i):
                EG[i,j] = -1
                EG[j,i] = 1
            else:
                EG[i,j] = 0
    return EG





##print(dStar(5))

from gurobipy import *
import numpy as np
from Projet_MOGPL.gameSim import generation_matrice
from Projet_MOGPL.proba import init_EG, E1, initPdk

memoD = {}
D=10
N=100
#Cette fonction prend en paramètres le vecteur de probabilités selon lequel joue P2
#ainsi que le nombre maximal de dés  et retourne la stratégie pure a adopter en vu de le battre dans la version en un coup de la variante simultanée
def optimization_sachantP2(P2,D):
    M = generation_matrice(D)
    M = M[1:,1:]
    if(len(P2) != D):
        raise Exception
    T = np.array([(M[i]*P2).sum() for i in range(0,D)])
    print(T)
    return T.argmax()




def resolution_systeme(D):
    variables = ["alpha"]
    variables = variables + ["p_" + str(i) for i in range(0, D)]
    m = Model("game_seq")
    var_model = {}
    for i in variables:
        if (i == "alpha"):
            var_model[i] = m.addVar(name=i, lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS)
        else:
            var_model[i] = m.addVar(name=i, lb=0, ub=1, vtype=GRB.CONTINUOUS)
    M = generation_matrice(D)
    M = M.T[1:, 1:]
    for i in range(0, D):
        m.addConstr(
            var_model["alpha"] <= np.array([M[i][j] * var_model["p_"+str(j)] for j in range(0,D)]).sum()
        )
        #m.addConstr(

    m.addConstr(np.array([var_model["p_"+str(j)] for j in range(0,D)]).sum() == 1)
    m.setObjective(var_model["alpha"], GRB.MAXIMIZE)
    m.optimize()
    P = [m.getVarByName(i).x for i in var_model]
    memoD[D] = P
    return P

distribution_probas = lambda D: memoD[D] if D in memoD else resolution_systemeD(D)

def tirer_nb_des(D):
    dist = distribution_probas(D)
    dist = np.array(dist)
    dist_c = np.array(dist)
    for i in range(0,len(dist)):
        dist_c[i] = dist[:i+1].sum()
    r = np.random.rand()
    print(dist_c)
    print(r)
    for i in range(0,len(dist_c)):
        if(r<=dist_c[i]):
            return i+1
    return i


#Ces fonctions utilisent gurobi afin de calculer la stratégie optimale a partir du nombre de dés (pour la
#version simplifiée  ou de la matrice de gain


def resolution_systemeD(D):
    print("Résolution d'un nouveau système par resolution systeme D")
    variables = ["alpha"]
    variables = variables + ["p_" + str(i) for i in range(0, D)]
    m = Model("game_seq")
    var_model = {}
    M = generation_matrice(D)
    for i in variables:
        if (i == "alpha"):
            var_model[i] = m.addVar(name=i, lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS)
        else:
            var_model[i] = m.addVar(name=i, lb=0, ub=1, vtype=GRB.CONTINUOUS)
    M = M[1:, 1:]
    for i in range(0, D):
        m.addConstr(
            var_model["alpha"] <= np.array([M[j][i] * var_model["p_"+str(j)] for j in range(0,D)]).sum()
        )
        #m.addConstr(

    m.addConstr(np.array([var_model["p_"+str(j)] for j in range(0,D)]).sum() == 1)
    m.setObjective(var_model["alpha"], GRB.MAXIMIZE)
    m.optimize()
    P = [m.getVarByName(i).x for i in var_model]
    memoD[D] = P

    return P


def resolution_systeme(M):
    variables = ["alpha"]
    variables = variables + ["p_" + str(i) for i in range(0, D)]
    m = Model("game_seq")
    var_model = {}
    for i in variables:
        if (i == "alpha"):
            var_model[i] = m.addVar(name=i, lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS)
        else:
            var_model[i] = m.addVar(name=i, lb=0, ub=1, vtype=GRB.CONTINUOUS)
    M = M.T[1:, 1:]
    for i in range(0, D):
        m.addConstr(
            var_model["alpha"] <= np.array([M[i][j] * var_model["p_"+str(j)] for j in range(0,D)]).sum()
        )
        #m.addConstr(

    m.addConstr(np.array([var_model["p_"+str(j)] for j in range(0,D)]).sum() == 1)
    m.setObjective(var_model["alpha"], GRB.MAXIMIZE)
    m.optimize()
    P = [m.getVarByName(i).x for i in var_model]
    memoD[D] = P
    return P[1:]


def resolution_systemeVal(M):
    global D
    global N
    variables = ["alpha"]
    variables = variables + ["p_" + str(i) for i in range(0, D)]
    m = Model("game_seq")
    m.setParam("OutputFlag",False)
    var_model = {}
    for i in variables:
        if (i == "alpha"):
            var_model[i] = m.addVar(name=i, lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS)
        else:
            var_model[i] = m.addVar(name=i, lb=0, ub=1, vtype=GRB.CONTINUOUS)
    M = M.T[1:, 1:]
    #print("M.Shape",M.shape)
    #print("Var model :" ,len(var_model))
    for i in range(0, D):
        m.addConstr(
            var_model["alpha"] <= np.array([M[i][j] * var_model["p_"+str(j)] for j in range(0,D)]).sum()
        )
        #m.addConstr(

    m.addConstr(lhs=np.array( [var_model["p_"+str(j)] for j in range(0,D)]).sum(),sense=GRB.EQUAL, rhs=1,name="proba")
    m.setObjective(var_model["alpha"], GRB.MAXIMIZE)
    m.optimize()
    P = [m.getVarByName(i).x for i in var_model]
    memoD[D] = P
    return var_model["alpha"].x,P




#for i in range(1,D+1):
#    for j in range(1,D+1):
#        E_ij[i,j] = E1(D,N,i,j,N,N,EG)


#Fonction qui calcule récursivement la matrice d'espérance de gain
def calculEG(i,j,N,D):
    global EG
    global E_ij
    if(i>N or j>N):
        return EG[i,j]
    if((i,j) in E_ij.keys()):
        return EG[i,j]
    else:
        calculEG(i + 1, j, N, D)
        calculEG(i, j + 1, N, D)
        calculEG(i + 1, j + 1,N,D)
        #print("Calcul pour i=",i,"j=",j)
        E_ij[(i, j)] = np.zeros((D + 1, D + 1))
        for k in range(1, D +1):
            for l in range(1, D+1 ):
                E_ij[(i, j)][k, l] = E1(D, N, k, l, i, j, EG)

        x,y = resolution_systemeVal(E_ij[(i, j)])
        print(" y = ",np.array(y).sum())
        print("stratégies = ",y[1:])
        print("E[",i,',',j,'] = ',x)
        EG[i, j] = x
        strat_ij[(i,j)] = y[1:]

#M = generation_matrice(3)
#print(resolution_systeme(M))

strat_ij = {}
E_ij = {}
EG = None
#Fonction qui calcule et qui enregistre les stratégies optimales
def remplir_strat(N,D):
    global EG
    import pandas as pd
    EG = init_EG(N,D)
    initPdk(D, N + 6 * D)
    calculEG(0,0,N,D)
    df = pd.DataFrame(EG)
    f = open("Esperance_facultative.html","w")
    print(f.write(df.to_html()))
    return EG

#remplir_strat(N,D)
import pandas as pd
#M = generation_matrice(3)
#print(resolution_systemeVal(M))
#calculEG(0,0,N,D)
#df = pd.DataFrame(strat_ij)
#print(strat_ij)

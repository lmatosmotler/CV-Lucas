# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:04:28 2022

@author: Lucas
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import minimize, rosen, rosen_der

class Beta:
    def __init__(self,nome):
        self.nome = nome
        self.B1 = 0
        self.B2 = 0
        self.B3 = 0


maturacao = range(1,120,1)

# =============================================================================
# curve,status = calibrate_ns_ols(vertices_mat,vertices_rend)
# print(curve)
# 
# =============================================================================
B = Beta("questao4")

def calc_Nelson_Sigel(labda):
    
    vertices_mat  = np.array([1,3,6,12,24,36,48,60,72,84,96,108,120])
    vertices_rend = np.array([0.0217,0.0247,0.0285,0.0339,0.0401,0.0431,0.0448,0.0458,0.0465,0.047,0.0474,0.0477,0.0479])

    vert_rend_100 = vertices_rend*100
    H = np.ones((len(vertices_mat),3))
    for j in range(0,len(vertices_mat),1):
       H[j][1] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])
       H[j][2] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])-np.exp(-labda*vertices_mat[j])
    HtH = np.dot(H.transpose(),H)
    HtH_1 = np.linalg.inv(HtH)
    matriz_final = np.dot(HtH_1,H.transpose())
# =============================================================================
#     calculando os parametros Beta
# =============================================================================
    beta = np.dot(matriz_final,vert_rend_100)
    beta = np.dot(matriz_final,vertices_rend)
    prev_NS = np.dot(H, beta)
    
        
    return prev_NS[len(prev_NS)-1]
        
res = minimize(calc_Nelson_Sigel,np.array([0]),method='BFGS',options={'gtol': 1e-4, 'disp': True})

print(res.x)

# =============================================================================
# labda_otim = 0.15143
# =============================================================================
def H_grande(labda, maturacao):
    H = np.ones((len(maturacao),3))
    for j in range(0,len(maturacao),1):
        H[j][1] = (1-math.exp(-labda*maturacao[j]))/(labda*maturacao[j])
        H[j][2] = (1-math.exp(-labda*maturacao[j]))/(labda*maturacao[j])-math.exp(-labda*maturacao[j])
    return H
# =============================================================================
#     print(H)
# =============================================================================






# =============================================================================
# print(nova_curva)
# =============================================================================

# =============================================================================
# Avalicao valor de face de um título
# =============================================================================



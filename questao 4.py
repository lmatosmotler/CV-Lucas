# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:04:28 2022
@author: Lucas
"""

import numpy as np
import math
import matplotlib.pyplot as plt


class Beta:
    def __init__(self,nome):
        self.nome = nome
        self.B1 = 0
        self.B2 = 0
        self.B3 = 0

vertices_mat  = np.array([1,3,6,12,24,36,48,60,72,84,96,108,120])
vertices_rend = np.array([0.0217,0.0247,0.0285,0.0339,0.0401,0.0431,0.0448,0.0458,0.0465,0.047,0.0474,0.0477,0.0479])

vert_rend_100 = vertices_rend*100

maturacao = np.ones(120)
for i in range(0,len(maturacao),1):
    if i == 0:
        maturacao[i] = 1
    else:
        maturacao[i] = (maturacao[i-1]+1) 

B = Beta("questao4")

def calc_Nelson_Sigel(vertices_mat,vertices_rend,vert_rend_100,B):
    precisao = 5
    labda_anterior = 0
    for i in range(0,10**precisao,1):
        labda = i/(10**precisao)
        H = np.ones((len(vertices_mat),3))
        for j in range(0,len(vertices_mat),1):
            H[j][1] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])
            H[j][2] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])-np.exp(-labda*vertices_mat[j])
        HtH = np.dot(H.transpose(),H)
        HtH_1 = np.linalg.inv(HtH)
        matriz_final = np.dot(HtH_1,H.transpose())
# =============================================================================
#         beta = np.dot(matriz_final,vert_rend_100)
# =============================================================================
        beta = np.dot(matriz_final,vertices_rend)
        prev_NS = np.dot(H, beta)
        erro_prev = vertices_rend - prev_NS
        erro = np.dot(erro_prev.transpose(), erro_prev)
        B.B1 = beta[0]*100
        B.B2 = beta[1]*100
        B.B3 = beta[2]*100
        if (erro < 0.00000001):
            return labda_anterior
        labda_anterior = labda
        
    return labda


labda_otim = calc_Nelson_Sigel(vertices_mat,vertices_rend,vert_rend_100,B)
beta_vec= np.array([B.B1,B.B2,B.B3])
print("\n\nLambda minha otimização: ",labda_otim)
B_certo = Beta("certo")


def param_excel(labda,vertices_mat,vertices_rend,vert_rend_100,B):
    H = np.ones((len(vertices_mat),3))
    for j in range(0,len(vertices_mat),1):
        H[j][1] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])
        H[j][2] = (1-np.exp(-labda*vertices_mat[j]))/(labda*vertices_mat[j])-np.exp(-labda*vertices_mat[j])
    HtH = np.dot(H.transpose(),H)
    HtH_1 = np.linalg.inv(HtH)
    matriz_final = np.dot(HtH_1,H.transpose())
    beta = np.dot(matriz_final,vert_rend_100)
    prev_NS = np.dot(H, beta)
    erro_prev = vert_rend_100 - prev_NS
    erro = np.dot(erro_prev.transpose(), erro_prev)
    B.B1 = beta[0]
    B.B2 = beta[1]
    B.B3 = beta[2]
    
    return beta
    
def H_grande(labda, maturacao):
    H = np.ones((len(maturacao),3))
    for j in range(0,len(maturacao),1):
        H[j][1] = (1-np.exp(-labda*maturacao[j]))/(labda*maturacao[j])
        H[j][2] = (1-np.exp(-labda*maturacao[j]))/(labda*maturacao[j])-np.exp(-labda*maturacao[j])
    
    return H

agazao = H_grande(0.15143, maturacao)
beta_vec_certo = param_excel(0.15143, vertices_mat, vertices_rend, vert_rend_100, B_certo)

nova_curva = np.dot(agazao,beta_vec_certo)

x = maturacao
y1 = vert_rend_100
y2 = nova_curva

plt.plot(x,y2)
plt.scatter(vertices_mat,vert_rend_100)

plt.show()


agazao1 = H_grande(labda_otim, maturacao)
curva_errada = np.dot(agazao1,beta_vec)

x1 = maturacao
y11 = vert_rend_100
y21 = curva_errada

print("\nETTJ minha otimização:")
print(curva_errada)
print("\nETTJ otimização Excel:")
print(nova_curva)

plt.plot(x1,y21)
plt.scatter(vertices_mat,vert_rend_100)

plt.show()

# =============================================================================
# Parte 2: Preço do Título
# =============================================================================

def avalia_titulo(face_value,prazo,cupom,pagamentos_anuais,nova_curva):
    cupom_anual = cupom*face_value
    preco = 0
    for i in range(0,prazo*pagamentos_anuais,1):
        if i == (prazo*pagamentos_anuais - 1):
            preco = preco + (face_value+cupom_anual/2)/((1+nova_curva[(i+1)*6-1]/100)**(i+1))
        else:
            preco = preco + (cupom_anual/2)/((1+nova_curva[(i+1)*6-1]/100)**(i+1))
    print("Título:")
    print("Valor de Face: ",face_value)
    print("Prazo: ",prazo)
    print("Taxa Cupom: ", cupom)
    print("Capitalização: Semestralmente")
    print("Preço: ",preco)
    


print("\n\n\n\n")
avalia_titulo(10000, 10, 0.05, 2, nova_curva)





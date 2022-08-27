# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:25:40 2022

@author: Lucas
"""
import numpy as np
import pandas as pd
import statistics
import math
from matplotlib import pyplot as plt

class Ativo:
    def __init__(self,name,info):
        self.nome = name
        self.dados = info
        self.media = 0
        self.desvio = 0
        self.coef_assim = 0
        self.curtose = 0
        self.pearson = 0
        self.jarque_bera = 0
        
    def mostra_ativo(self):
        print("\nNome: ",self.nome)
        print("Media: ",self.media)
        print("Desvio Padrao: ",self.desvio)
        print("Coeficiente de Assimetria: ", self.coef_assim)
        print("Coeficiente de Curtose: ",self.curtose)
        print("Coeficiente de Jarque Bera: ",self.jarque_bera)
        
    def calc_media(self):
        self.media = statistics.mean(self.dados['Close'])
    
    def calc_desvio(self):
        self.desvio = self.dados['Close'].std()
        
    def calc_assimetria(self):
        n = self.dados.shape[0]
        A = 0
        for i in range(0,n,1):
            A = A + math.pow(((self.dados.loc[i,'Close'])-self.media)/self.desvio,3)
        A = A*n/((n-1)*(n-2))
        self.coef_assim = A
        
    def calc_curtose(self):
        n = self.dados.shape[0]
        K = 0
        for i in range (0,n,1):
            K = K + math.pow(((self.dados.loc[i,'Close'])-self.media)/self.desvio,4)
        K = K*(n*(n+1))/((n-1)*(n-2)*(n-3))-(3*(n+1)*(n+1))/((n-2)*(n-3))
        self.curtose = K
    
    def calc_j_bera(self):
        n = self.dados.shape[0]
        self.jarque_bera = (n/6)*(self.coef_assim*self.coef_assim+((self.curtose-3)*(self.curtose-3)/4))


class Portfolio:
    def __init__(self,nome,ativo1,ativo2):
        self.nome = nome
        self.ativo1 = ativo1
        self.ativo2 = ativo2
        self.pearson = 0
    
    def mostra_port(self):
        print("\n\n")
        print("Nome do Portfolio: ",self.nome)
        print("Coeficiente de Pearson: ",self.pearson)
        print("\nAtivo 1:\n")
        self.ativo1.mostra_ativo()
        print("Ativo 2:\n")
        self.ativo2.mostra_ativo()
        

    def calc_pearson(self):
        covar = np.cov(self.ativo1.dados.loc[:,'Close'],self.ativo2.dados.loc[:,'Close'])
        pearson1 = covar[0][1]/(self.ativo1.media*self.ativo2.media)
        print("Pearson: ", pearson1)
        self.pearson = pearson1

# =============================================================================
# Baixando os dados do csv...
# =============================================================================

vale_data = pd.read_csv('VALE.csv')
print(vale_data.columns)
vale_data['Close'] = vale_data['Close'].apply(math.log)


nflx_data = pd.read_csv('NFLX.csv')
print(nflx_data.columns)
nflx_data['Close'] = nflx_data['Close'].apply(math.log)

# =============================================================================
# Criando os ativos
# =============================================================================

vale = Ativo("VALE3",vale_data)
nflx = Ativo("NFLX",nflx_data)

# =============================================================================
# Criando portfolio e colocando os ativos dentro do portfolio
# =============================================================================

port = Portfolio("questao2", vale, nflx)

# =============================================================================
# Mostrando Variação dos Ativos
# =============================================================================

plt.rcParams["figure.figsize"] = [7.00, 7.00]
plt.rcParams["figure.autolayout"] = True
vale.dados['Close'].plot()
nflx.dados['Close'].plot()
plt.show()


# =============================================================================
# Calculando índices
# =============================================================================


vale.calc_media()
vale.calc_desvio()
vale.calc_assimetria()
vale.calc_curtose()
vale.calc_j_bera()

nflx.calc_media()
nflx.calc_desvio()
nflx.calc_assimetria()
nflx.calc_curtose()
nflx.calc_j_bera()

port.calc_pearson()

# =============================================================================
# Mostrando Ativos e Índices
# =============================================================================

# =============================================================================
# vale.mostra_ativo()
# nflx.mostra_ativo()
# =============================================================================

port.mostra_port()







# -*- coding: utf-8 -*-
"""
Created on Sun May  1 22:07:07 2022

@author: Lucas
"""

import numpy as np
import pandas as pd
import statistics
import math
from matplotlib import pyplot as plt

R_F = pow((1+0.05),1/252)-1

SIGMA_1_SQR = 0.24906469026390324**2
MI_1 = 2.5705204371508654

SIGMA_2_SQR = 0.3737060228813233**2
MI_2 = 5.874763648122682

RO_12 = 0.0031672537148864834

GAMMA = 2.85

Saldo_atual = 1000000
percentil_corte = 0.05
coef_confianca = 1 - percentil_corte



#criação do objeito Portfolio
class Portfolio:
    def __init__(self,name):
        self.name = name
        self.alfa = 0
        self.beta = 0
        self.gamma = 0
        self.retorno_esperado_var_min = 0
        self.desvio_padrao_var_min = 0
        self.peso1_var_min = 0
        self.peso2_var_min = 0
        self.retorno_esperado_tan = 0
        self.desvio_padrao_tan = 0
        self.peso1_tan = 0
        self.peso2_tan = 0
        self.retorno_esperado_invest = 0
        self.desvio_padrao_invest = 0
        self.peso1_invest = 0
        self.peso2_invest = 0

        
    def mostra_portfolio(self):
        print("\n** DADOS DO PORTFOLIO **") 
        print("\tNome do Portfolio: ",self.name)
        print("\tAlfa: ",self.alfa)
        print("\tBeta: ",self.beta)
        print("\tGamma: ", self.gamma)
        print("\n** Estrategia de Alocacao: **")
        print("\n *Variância Mínima:*")
        print("\tRetorno Esperado Variancia Minima: ", self.retorno_esperado_var_min)
        print("\tDesvio Padrao Variancia Minima: ",self.desvio_padrao_var_min)
        print("\tW1 Variancia minima: ",self.peso1_var_min)
        print("\tW2 Variancia minima: ",self.peso2_var_min)
        print("\n *Portfólio Tangente: *")
        print("\tRetorno Esperado Portfolio Tangente: ", self.retorno_esperado_tan)
        print("\tDesvio Padrao Portfolio Tangente: ",self.desvio_padrao_tan)
        print("\tW1 Portfolio Tangente: ",self.peso1_tan)
        print("\tW2 Portfolio Tangente: ",self.peso2_tan)
        print("\n *Portfólio Geral do Investidor:*")
        print("\tRetorno Esperado Portfolio geral do Investidor: ", self.retorno_esperado_invest)
        print("\tDesvio Padrao Portfolio geral do Investidor: ",self.desvio_padrao_invest)
        print("\tW1 Portfolio Investidor: ",self.peso1_invest)
        print("\tW2 Portfolio Investidor: ",self.peso2_invest,"\n")
    #Cálculo de alfa, beta e gamma, essencialmente as equações (18), (19) e (20) da aula 01


#criação do objeto ativo
class Ativo:
    def __init__(self, name, mi, sigma):
        self.name = name
        self.mi = mi
        self.sigma = sigma
    #função para facilitar a visualização dos ativos
    def mostra_ativo(self):
        print("\n")
        print("Nome do Ativo: ")
        print(self.name)
        print("Mi do Ativo: ")
        print(self.mi)
        print("Sigma quadrado do Ativo: ")
        print(self.sigma)
        print("\n")

    

#Criando o portfolio
port = Portfolio("Lista 1")

#criação dos dois ativos do problema
ativo1 = Ativo("Vale",MI_1,SIGMA_1_SQR)
ativo2 = Ativo("Netflix",MI_2,SIGMA_2_SQR)

ativo1.mostra_ativo()
ativo2.mostra_ativo()


#Cálculo de alfa, beta e gamma do portfolio
def alpha(ativo1,ativo2,corr):
    return (ativo1.sigma + ativo2.sigma - 2*np.sqrt(ativo1.sigma)*np.sqrt(ativo2.sigma)*corr)/((ativo2.mi - ativo1.mi)*(ativo2.mi - ativo1.mi))
    
def beta (ativo1, ativo2,corr):
    return -2*(ativo1.mi*ativo2.sigma + ativo2.mi*ativo1.sigma - (ativo1.mi + ativo2.mi)*np.sqrt(ativo1.sigma)*np.sqrt(ativo2.sigma)*corr)/((ativo1.mi - ativo2.mi)*(ativo1.mi - ativo2.mi))

def gamma (ativo1,ativo2,corr):
    return ((ativo1.mi*ativo1.mi)*ativo2.sigma + (ativo2.mi*ativo2.mi)*ativo1.sigma - 2*ativo1.mi*ativo2.mi*np.sqrt(ativo1.sigma)*np.sqrt(ativo2.sigma)*corr)/((ativo1.mi - ativo2.mi)*(ativo1.mi - ativo2.mi))
    
#calculo da alocacao de variancia minima
def var_minima (ativo1,ativo2,portfolio):
    alfa_min = portfolio.alfa
    beta_min = portfolio.beta
    gamma_min = portfolio.gamma
    retorno_esperad_minimo = -beta_min/(2*alfa_min)
    desvio_pad_min = np.sqrt(gamma_min - (beta_min*beta_min/(4*alfa_min)))
    print("\n** Portfolio de Variancia Minima: **")
    print("Retorno Esperado Variancia Minima: ",retorno_esperad_minimo)
    print("Desvio Padrao Variancia Minima: ",desvio_pad_min)
    port.desvio_padrao_var_min = desvio_pad_min
    port.retorno_esperado_var_min = retorno_esperad_minimo
    w1 = (retorno_esperad_minimo - ativo2.mi)/(ativo1.mi - ativo2.mi)
    w2 = (ativo1.mi - retorno_esperad_minimo)/(ativo1.mi - ativo2.mi)
    portfolio.peso1_var_min = w1
    portfolio.peso2_var_min = w2
    print("\n Pesos:\n")
    print("w1: ")
    print(w1)
    print("\nw2: ")
    print(w2)
    
#calculo do portfolio tangente
def tangente (ativo1,ativo2,port):
    alfa = port.alfa
    beta = port.beta
    gamma = port.gamma
    retorno_esperado_estrela = -(beta*R_F + 2*gamma)/(2*alfa*R_F+beta)
    desvio_padrao_estrela = np.sqrt(alfa*retorno_esperado_estrela*retorno_esperado_estrela+beta*retorno_esperado_estrela+gamma)
    print("\n** Portfolio Tangente: **")
    print("Retorno Esperado Portfolio Tangente: ", retorno_esperado_estrela)
    print("Desvio Padrao Portfolio Tangente: ", desvio_padrao_estrela)
    w1 = (retorno_esperado_estrela - ativo2.mi)/(ativo1.mi - ativo2.mi)
    w2 = (ativo1.mi - retorno_esperado_estrela)/(ativo1.mi - ativo2.mi)
    port.peso1_tan = w1
    port.peso2_tan = w2
    print("\n Pesos:\n")
    print("w1: ")
    print(w1)
    print("\nw2: ")
    print(w2)
    port.desvio_padrao_tan = desvio_padrao_estrela
    port.retorno_esperado_tan =  retorno_esperado_estrela
    
#calculo do portfolio geral do investidor considerando o portfolio tangente
def investidor (ativo1,ativo2,port):
    sharpe = (port.retorno_esperado_tan - R_F)/port.desvio_padrao_tan
    w1_estrela = (1/GAMMA)*sharpe/port.desvio_padrao_tan #peso do portfolio em si, ou seja, não risk free
    w2_risk_free = 1-w1_estrela
    port.peso1_invest = w1_estrela
    port.peso2_invest = w2_risk_free
    retorno_esperado_investidor = w1_estrela*(port.retorno_esperado_tan-R_F)+R_F
    desvio_padrao_investidor = max(((retorno_esperado_investidor-R_F)/(port.retorno_esperado_tan-R_F))*port.desvio_padrao_tan,-((retorno_esperado_investidor-R_F)/(port.retorno_esperado_tan-R_F))*port.desvio_padrao_tan)
    print("\n** Portfolio Geral do Investidor: **")
    print("Sharpe: ", sharpe)
    print("Peso Investimentos: ", w1_estrela)
    print("Peso Ativo Livre de Risco: ", w2_risk_free)
    print("Retorno Esperado Implicito: ", retorno_esperado_investidor)
    print("Desvio padrão implicito: ",desvio_padrao_investidor)
    port.retorno_esperado_invest = retorno_esperado_investidor
    port.desvio_padrao_invest = desvio_padrao_investidor


port.alfa = alpha(ativo1, ativo2, RO_12)
port.beta = beta(ativo1, ativo2, RO_12)
port.gamma = gamma(ativo1, ativo2, RO_12)


    
a = var_minima(ativo1, ativo2,port)
b = tangente(ativo1, ativo2, port)
c = investidor(ativo1, ativo2, port)
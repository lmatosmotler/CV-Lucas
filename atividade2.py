# -*- coding: utf-8 -*-
"""
Created on Mon May 23 23:48:47 2022

@author: Lucas
"""
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import NormalDist
from matplotlib import cm
from scipy.stats import norm
import numpy as np
import math
import tabulate
import time



class Option:
    def __init__(self,nome,n,S_0,K,T,u,d,r,q):
        self.name = nome
        self.n = n
        self.S_0 = S_0
        self.K = K
        self.T = T
        self.u = u
        self.d = d
        self.r = r
        self.q = q
        
    def mostra_option(self):
        print("Nome: ",self.name)
        print("Numero de períodos: ",self.n)
        print("Preço Inicial: ",self.S_0)
        print("Preço do Exercício: ", self.K)
        print("Maturiry: ",self.T)
        print("Ganho no cenários up: ",self.u)
        print("Perda no cenário down: ",self.d)
        print("Risk Free Rate: ",self.r)
        print("q = ",self.q)
        

class BlackScholes:
    def __init__(self,nome,S_0,K,T,r,alfa,mi,sigma):
        self.nome = nome
        self.S_0 = S_0
        self.K = K
        self.T = T
        self.r = r
        self.a = alfa
        self.mi = mi
        self.sigma = sigma
        
    def mostra_BS(self):
        print("Nome ativo: ",self.nome)
        print("Preço inicial: ",self.S_0)
        print("Preço strike: ",self.K)
        print("Maturity: ",self.T)
        print("Risk Free Rate: ",self.r)
        print("Alfa: ",self.a)
        print("Mi: ",self.mi)
        print("Sigma: ",self.sigma)
        
class OptionPricing:

    def __init__(self,S0,E,T,rf,a,sigma,iterations):
    
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.a = a
        self.sigma = sigma
        self.iterations = iterations
        self.var = 0
    
    def call_option_simulation(self):
    
        option_data = np.zeros([self.iterations, 2])
        rand = np.random.normal(0,1, [1, self.iterations])
        stock_price = self.S0*np.exp(self.T*(self.rf -self.a - 0.5*self.sigma**2) + self.sigma * np.sqrt(self.T) * rand)
        option_data[:,1] = stock_price - self.E
        var = np.var(option_data[:,1])
        self.var = var
        
        # average for the Monte Carlo Method
        average = np.sum(np.amax(option_data, axis = 1))/float(self.iterations)
        
        return np.exp(-1.0*self.rf*self.T) * average
    
    def put_option_simulation(self):
    
        option_data = np.zeros([self.iterations,2])
        rand = np.random.normal(0,1,[1,self.iterations])
        stock_price = self.S0*np.exp(self.T*(self.rf -self.a - 0.5*self.sigma**2) + self.sigma * np.sqrt(self.T) * rand)
        option_data[:,1] = self.E - stock_price
        var = np.var(option_data)
        self.var = var
        
        # average for the Monte Carlo Method
        average = np.sum(np.amax(option_data, axis = 1))/float(self.iterations)
        
        return np.exp(-1.0*self.rf*self.T) * average



def option_q(opcao):
    return (math.exp(opcao.r*(opcao.T/opcao.n)) - opcao.d)/(opcao.u - opcao.d)

def cria_option():
    nome = input("Nome do Ativo: ")
    n = int(input("Qunatidade de períodos: "))
    S_0 = float(input("Preço inicial: "))
    K = float(input("Preço do exercício: "))
    T = float(input("Maturidade/Vencimento: "))
    u = float(input("Ganho do outcome positivo: "))
    d = float(input("Perda do outcome negativo: "))
    r = float(input("Risk free Rate: "))
    ativo = Option(nome, n, S_0, K, T, u, d, r, 0)
    q = option_q(ativo)
    ativo.q = q
    return ativo

def binomial(opcao):
    soma = 0
    n = opcao.n
    q = opcao.q
    u = opcao.u
    d = opcao.d
    S0 = opcao.S_0
    K = opcao.K
    T = opcao.T
    r = opcao.r
    for j in range(0,opcao.n+1,1):
        maior = max(pow(u, j)*pow(d, n-j)*S0-K,0)
        soma = soma + (math.factorial(n)/(math.factorial(j)*math.factorial(n-j)))*pow(q,j)*pow(1-q, n-j)*maior
    valor = soma*math.exp(-1*r*T)
    return valor
        

# =============================================================================
# 
# call = cria_option()
# call.mostra_option()
# valor_call = binomial(call)
# print("A Call vale: ",valor_call)
# =============================================================================

def cria_BS():
    nome = input("Nome do Ativo: ")
    S_0 = float(input("Preço inicial: "))
    K = float(input("Preço do exercício: "))
    T = float(input("Maturidade/Vencimento: "))
    r = float(input("Risk free Rate: "))
    a = float(input("Insira taxa de dividendos: "))
    mi = float(input("Retorno Subjacente: "))
    sig = float(input("Volatilidade do Preço: "))
    ativo = BlackScholes(nome, S_0, K, T,r,a,mi,sig)
    return ativo

def N(x):
    med = 0
    desv = 1
    resp= math.exp(-(x*x)/(2*desv*desv))/(math.sqrt(2*math.pi*1))
    return resp

def black_scholes(opcao):
    alf = opcao.a
    S0 = opcao.S_0
    K = opcao.K
    T = opcao.T
    r = opcao.r
    sig = opcao.sigma
    d_1 = (math.log(S0/K)+(r - alf + 0.5*sig*sig)*T)/(sig*math.sqrt(T))
# =============================================================================
#     print("D1: ",d_1)
# =============================================================================
    d_2 = d_1 - sig*math.sqrt(T)
# =============================================================================
#     print("Normal d1: ",norm.cdf(d_1))
# =============================================================================
    C = S0*math.exp(-alf*T)*norm.cdf(d_1)-K*math.exp(-r*T)*norm.cdf(d_2)
    print("Valor da Call de BalckScholes é: ", C)
    return C
    
# =============================================================================
# black = cria_BS()
# black.mostra_BS()
# valor_bs = black_scholes(black)
# =============================================================================






def cria_MC():
    S_0 = 60
    E = 60
    T = 60/252
    rf = 0.06
    a = 0.01
    sig = 0.3
    
    BS_anal = BlackScholes("Analitico", S_0, E, T,rf,a,0.08,sig)
    BS_MC_1 = OptionPricing(S_0,E,T,rf,a,sig,1000)
    BS_MC_2 = OptionPricing(S_0,E,T,rf,a,sig,2000)
    BS_MC_5 = OptionPricing(S_0,E,T,rf,a,sig,5000)
    BS_MC_10 = OptionPricing(S_0,E,T,rf,a,sig,10000)
    BS_MC_50 = OptionPricing(S_0,E,T,rf,a,sig,50000)
    BS_MC_100 = OptionPricing(S_0,E,T,rf,a,sig,100000)
    
    valor_teo = black_scholes(BS_anal)
    MC_1 = BS_MC_1.call_option_simulation()
    MC_2 = BS_MC_2.call_option_simulation()
    MC_5 = BS_MC_5.call_option_simulation()
    MC_10 = BS_MC_10.call_option_simulation()
    MC_50 = BS_MC_50.call_option_simulation()
    MC_100 = BS_MC_100.call_option_simulation()
    dados = [
        ["1000",valor_teo,MC_1,MC_1-1.96*math.sqrt(BS_MC_1.var)/math.sqrt(1000),MC_1+1.96*math.sqrt(BS_MC_1.var)/math.sqrt(1000),(abs(MC_1-valor_teo)/valor_teo)*100],
        ["2000",valor_teo,MC_2,MC_2-1.96*math.sqrt(BS_MC_2.var)/math.sqrt(2000),MC_2+1.96*math.sqrt(BS_MC_2.var)/math.sqrt(2000),(abs(MC_2-valor_teo)/valor_teo)*100],
        ["5000",valor_teo,MC_5,MC_5-1.96*math.sqrt(BS_MC_5.var)/math.sqrt(5000),MC_5+1.96*math.sqrt(BS_MC_5.var)/math.sqrt(5000),(abs(MC_5-valor_teo)/valor_teo)*100],
        ["10000",valor_teo,MC_10,MC_10-1.96*math.sqrt(BS_MC_10.var)/math.sqrt(10000),MC_10+1.96*math.sqrt(BS_MC_10.var)/math.sqrt(10000),(abs(MC_10-valor_teo)/valor_teo)*100],
        ["50000",valor_teo,MC_50,MC_50-1.96*math.sqrt(BS_MC_50.var)/math.sqrt(50000),MC_50+1.96*math.sqrt(BS_MC_50.var)/math.sqrt(50000),(abs(MC_50-valor_teo)/valor_teo)*100],
        ["100000",valor_teo,MC_100,MC_100-1.96*math.sqrt(BS_MC_100.var)/math.sqrt(100000),MC_100+1.96*math.sqrt(BS_MC_100.var)/math.sqrt(100000),(abs(MC_100-valor_teo)/valor_teo)*100],
        ]
# =============================================================================
#     print(dados)
# =============================================================================
    head = ["Iterações","Valor Analítico","Valor Numérico","Limite Inferio","Limite Superior","Erro%"]
    print(tabulate(dados, headers=head, tablefmt="grid"))
    
    

cria_MC()



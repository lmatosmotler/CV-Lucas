# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 16:36:33 2022
@author: Lucas
"""
#import das bibliotecas necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import NormalDist
from matplotlib import cm

#parametros do problema
R_F = 0.05

SIGMA_1_SQR = 0.09
MI_1 = 0.12

SIGMA_2_SQR = 0.25
MI_2 = 0.25

RO_12 = 0.25

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
ativo1 = Ativo("A",MI_1,SIGMA_1_SQR)
ativo2 = Ativo("B",MI_2,SIGMA_2_SQR)

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



#Calculos do problema 1
port.alfa = alpha(ativo1, ativo2, RO_12)
port.beta = beta(ativo1, ativo2, RO_12)
port.gamma = gamma(ativo1, ativo2, RO_12)


    
a = var_minima(ativo1, ativo2,port)
b = tangente(ativo1, ativo2, port)
c = investidor(ativo1, ativo2, port)

alfa_original = port.alfa
beta_original = port.beta
gamma_original = port.gamma

plt.rcParams["figure.figsize"] = [7.00, 7.00]
plt.rcParams["figure.autolayout"] = True
x_invest = port.desvio_padrao_invest
x_tan = port.desvio_padrao_tan
x_var_min = port.desvio_padrao_var_min

y_invest = port.retorno_esperado_invest
y_tan = port.retorno_esperado_tan
y_var_min = port.retorno_esperado_var_min


#gráficos do problema

fronteira_eficiente = pd.DataFrame(columns = ['desvio','retorno'])
linha_alocacao = pd.DataFrame(columns = ['desvio','retorno'])
curva_utilidade = pd.DataFrame(columns = ['desvio','retorno'])



def calc_sigma(port,mi):
    return np.sqrt((port.gamma-port.beta*port.beta/(4*port.alfa))*(1+(((mi+port.beta/(2*port.alfa))*(mi+port.beta/(2*port.alfa)))/((1/port.alfa)*(port.gamma-port.beta*port.beta/(4*port.alfa))))))

def calc_mi(port,sigma):
    a = port.alfa
    b = port.beta
    g = port.gamma
    return (np.sqrt((1/a)*(g-(b*b/(2*a)))*(sigma*sigma/(g-(b*b/(4*a)))-1))-(b/(2*a)))

def cria_curvas_fronteira(fronteira,port,ativo1,ativo2):
    cmap = cm.get_cmap("summer")
    rng = np.linspace(0,1, 100)[::-1]
    fig,ax=plt.subplots()
    k = 0
    for i in range(-100,102,2):
        corr = i/100
        port.alfa = alpha(ativo1, ativo2,corr)
        port.beta = beta(ativo1, ativo2,corr)
        port.gamma = gamma(ativo1, ativo2,corr)
        
        temp_comp = pd.DataFrame([[calc_sigma(port,0),0]],columns = ['desvio','retorno'])
        for j in range(1,121,1):
            mi = j/400
            temp = pd.DataFrame([[calc_sigma(port,mi),mi]],columns = ['desvio','retorno'])
            fronteira = pd.concat([fronteira,temp])
            temp_comp = pd.concat([temp_comp,temp])
# =============================================================================
#             if j == 120 and corr != 0.25:
#                 temp.plot(kind = 'line',x = 'desvio',y = 'retorno')
# =============================================================================
                #fronteira = pd.DataFrame(columns = ['desvio','retorno']
        ax.plot(temp_comp['desvio'],temp_comp['retorno'],ls='-')
        k = k+1
    plt.show()
    return fronteira
    

def cria_linha_alocacao(port):
    mi = port.retorno_esperado_tan
    sigma = port.desvio_padrao_tan
    print("\n\nRetorno Esperado do Tangente: ",mi)
    print("Desvio padrão do Tangente: ",sigma)
    linha = pd.DataFrame([[0,(((mi-R_F)/sigma)*0+R_F)]],columns = ['desvio','retorno'])
    for i in range(1,71,1):
        sigma_aloc = i/100
        temp = pd.DataFrame([[sigma_aloc,(((mi-R_F)/sigma)*sigma_aloc+R_F)]],columns = ['desvio','retorno'])
        linha = pd.concat([linha,temp])
    plt.plot(linha['desvio'], linha['retorno'],color = 'midnightblue')
    return linha

def funcao_utilidade(port):
    mi = port.retorno_esperado_invest
    sigma =  port.desvio_padrao_invest
    print("\n\nRetorno Esperado Investidor: ",mi)
    print("Desvio Padrao Investidor: ",sigma)
    utilidade = pd.DataFrame([[0,mi+(GAMMA/2)*(-sigma*sigma)]],columns = ['desvio','retorno'])
    for i in range(1,71,1):
        sigma_aloc = i/100
        temp = pd.DataFrame([[sigma_aloc,mi+(GAMMA/2)*(-sigma*sigma+sigma_aloc*sigma_aloc)]],columns = ['desvio','retorno'])
        utilidade = pd.concat([utilidade,temp])
    plt.plot(utilidade['desvio'], utilidade['retorno'], color = 'red')
    
    
def plota_fronteira_eficiente (port):
    corr = 0.25
    port.alfa = alpha(ativo1, ativo2,corr)
    port.beta = beta(ativo1, ativo2,corr)
    port.gamma = gamma(ativo1, ativo2,corr)
    new = pd.DataFrame([[calc_sigma(port,0),0]],columns = ['desvio','retorno'])
    for j in range(0,121,1):
      mi = j/400
      temp = pd.DataFrame([[calc_sigma(port,mi),mi]],columns = ['desvio','retorno'])
      new = pd.concat([new,temp])
      if j == 120 :
          new.plot(kind = 'line',x='desvio',y='retorno',color = 'orange')

fronteira_eficiente = cria_curvas_fronteira(fronteira_eficiente, port, ativo1, ativo2)

plota_fronteira_eficiente(port)

linha_alocacao = cria_linha_alocacao(port)

utilidade = funcao_utilidade(port)

port.alfa = alpha(ativo1, ativo2,0.25)
port.beta = beta(ativo1, ativo2,0.25)
port.gamma = gamma(ativo1, ativo2,0.25)


plt.plot(x_invest,y_invest,marker="o",markersize=10,markerfacecolor="green", label ="port. investidor")
plt.plot(x_tan,y_tan,marker="o",markersize=10,markerfacecolor="red", label ="port. tangente")
plt.plot(x_var_min,y_var_min,marker="o",markersize=10,markerfacecolor="blue", label ="port. var. min.")
plt.plot(0,R_F,marker="o",markersize=10,markerfacecolor="black", label ="Risk Free")
plt.xlim([0,0.6])
plt.ylim([0,0.3])
plt.show()


print("\n** Parâmetros originais (Ro = 0,25): **\n")
print("\tAlfa: ",alfa_original)
print("\tBeta: ",beta_original)
print("\tGamma: ",gamma_original)

port.mostra_portfolio()

fi = NormalDist(0,1).inv_cdf(percentil_corte)
print("** Value at Risk **")
print("\tFi: ",fi)

VaR = -Saldo_atual*(port.retorno_esperado_invest+port.desvio_padrao_invest*fi)

print("\tVaR: ", VaR)
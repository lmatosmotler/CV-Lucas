#!/usr/bin/env python
from tkinter import *
from datetime import datetime
   
def number_of_days(date_1, date_2):  
    return (date_2 - date_1).days  

def clicou_nao():
    messagebox.showinfo(":(", "Eu te amo muito... independetemente do que aconteça eu estou com saudade de você")
    
def clicou_sim():
    date_1 = datetime(2023, 1, 28,0,0,0)  
    date_2 = datetime.today()
    messagebox.showinfo("Eu também tô!!! Faltam ",number_of_days(date_2, date_1))

top = Tk()
top.geometry("400x75")
top.title('Oi pitchuquiña, tá com saudade de mim?')

    
b1 = Button(top,text = "SIM",command = clicou_sim,activeforeground = "green",activebackground = "pink")
b1.pack(side = LEFT, pady=10,padx=30)
  
b2 = Button(top,text = "NAO",command = clicou_nao,activeforeground = "red",activebackground = "pink")
b2.pack(side = LEFT, pady=10,padx=130)
      
      
    
top.mainloop()  



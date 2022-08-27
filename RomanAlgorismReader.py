#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 01:19:30 2022

@author: lucasmolter
"""
#Function to read roman integers
def roman_reader(s):
    values = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    soma = 0
    prev = 'M'
    prev_value = 0
    for i in s:
        if values[i]>values[prev]:
            soma = soma - 2*prev_value + values[i]
        else:
            soma = soma + values[i]
        prev = i
        prev_value = values[i]
    return soma

#Tests

s1 = "III"
s2 = "LVIII"
s3 = "MCMXCIV"

teste = 0

if roman_reader(s1)==3:
    print("Test 1: pass")
    teste = teste + 1
    
if roman_reader(s2)==58:
    print("Test 2: pass")
    teste = teste + 1

if roman_reader(s3)==1994:
    print("Test 3: pass")
    teste = teste + 1

if teste == 3:
    print("All tests passed")
else:
    print("Test Failed")
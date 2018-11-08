# -*- coding: utf-8 -*-

import math
import pprint

def trata_linha(linha):
    return linha.replace("\"", "").replace("\n", "").replace("ã", "a").replace("ç", "c").replace("í", "i").replace("é", "e").replace("ó", "o").split(",")

def totais_col(idx, matriz):
    totais = []
    for linha in matriz:
        for i, valor in enumerate(linha):
            if i == idx and valor not in totais:
                totais.append(valor)
    return {val: 0.0 for val in totais}

def entropia(resultados):
    valores = resultados.values()
    total = sum(valores)
    entropia = 0.0
    for res in valores:
        if not (res == 0):
            entropia += -(res/total)*math.log(res/total, 2)
    return entropia

def struct(matriz, colunas):
    totais = {col: totais_col(idx, matriz) for idx, col in enumerate(colunas)}
    for linha in matriz:
        for idx, val in enumerate(linha):
            totais[colunas[idx]][val] += 1
    return totais



def entropias_e_sub_matrizes(matriz, colunas):
    entropias = {}
    sub_matrizes = {}
    for atributo, valores in totais.items():
        sub_matrizes[atributo] = {}
        entropias[atributo] = {}
        for valor in valores.keys():
            sub_matrizes[atributo][valor] = []
            entropias[atributo][valor] = 0
            for linha in matriz:
                for linha_val in linha:
                    if(linha_val == valor):
                        sub_matrizes[atributo][valor].append(linha)
            entropias[atributo][valor] = entropia(struct(sub_matrizes[atributo][valor], colunas)[colunas[-2]])
    return [entropias, sub_matrizes]

def ganhos(entropia_total, sub_matrizes, entropias, totais):
    ganhos = {}
    for atributo, valores in entropias.items():
        ganhos[atributo] = ganho(entropia_total, sub_matrizes[atributo], entropias[atributo], totais[atributo])
    return ganhos

def ganho(entropia_total, entropias_valores, totais_valores):
    ganho = entropia_total
    for i in xrange(0,len(entropias_valores)):
        proporcao = totais_valores[i]/sum(totais_valores)
        if(proporcao!=0):
            ganho += -proporcao*math.log(proporcao, 2)*entropias_valores[i]
    return ganho

def ganhos(entropias, totais, entropia_total):
    ganhos = {}
    for atributo in entropias.keys(): 
        entropias_valores = entropias[atributo].values()
        totais_valores = totais[atributo].values()
        ganhos[atributo] = ganho(entropia_total, entropias_valores, totais_valores)
    return ganhos

def ap(s):
    pp.pprint(s)

pp = pprint.PrettyPrinter(indent=4)
file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:]))
totais = struct(matriz, colunas)
resultados = totais[colunas[-2]]
entropia_total = entropia(resultados)
entropias_e_sub_matrizes = entropias_e_sub_matrizes(matriz, colunas)
entropias = entropias_e_sub_matrizes[0]

ganhos = ganhos(entropias, totais, entropia_total)
max(ganhos, key=ganhos.get)
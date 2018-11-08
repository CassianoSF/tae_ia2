# -*- coding: utf-8 -*-

import math
import pprint

def trata_linha(linha):
    vals = linha.replace("\"", "").replace("\n", "").replace("ã", "a").replace("ç", "c").replace("í", "i").replace("é", "e").replace("ó", "o").split(",")
    return [val.strip() for val in vals] 

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



def entropias_e_sub_matrizes(matriz, colunas, totais):
    entropias = {}
    sub_matrizes = {}
    for atributo, valores in totais.items():
        if(atributo != 'voto'):
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
        if(atributo != 'voto'):
            entropias_valores = entropias[atributo].values()
            totais_valores = totais[atributo].values()
            ganhos[atributo] = ganho(entropia_total, entropias_valores, totais_valores)
    return ganhos

def resultado_formatado(lst):
        mais_comun = max(lst, key=lst.count)
        qtd = lst.count(mais_comun)
        return str((qtd*1.0)/len(lst)) + mais_comun

def calcula_branch(matriz, colunas):
    if (len(colunas) == 1):
        return resultado_formatado(matriz)
    # if (len(matriz) == 1):
    #     return matriz
    totais = struct(matriz, colunas)
    resultados = totais['voto']
    entropia_total = entropia(resultados)
    ent_sub = entropias_e_sub_matrizes(matriz, colunas, totais)
    entropias = ent_sub[0]
    sub_matrizes = ent_sub[1]
    _ganhos = ganhos(entropias, totais, entropia_total)
    maior_ganho = max(_ganhos, key=_ganhos.get)
    if (maior_ganho == 'voto'):
        return resultado_formatado(matriz)
    arvore = {}
    index = colunas.index(maior_ganho)
    colunas = list(filter(lambda x: x != maior_ganho, colunas))
    for val in sub_matrizes[maior_ganho].keys():
        for linha in sub_matrizes[maior_ganho][val]:
            if (len(linha)>index and maior_ganho != 'voto' and len(linha) > 1):
                linha.remove(linha[index])
        arvore[val] = calcula_branch(sub_matrizes[maior_ganho][val], colunas)
    if (len(arvore.keys()) == 0):
        return resultado_formatado(matriz)
    if (len(arvore.keys()) == 1):
        return arvore[arvore.keys()[0]]
    return arvore


def ap(s):
    pp.pprint(s)

pp = pprint.PrettyPrinter(indent=4)
file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:]))
arvore = calcula_branch(matriz, colunas)
ap(arvore)

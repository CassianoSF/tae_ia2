# -*- coding: utf-8 -*-

import math
import pprint

from sklearn.datasets import load_breast_cancer
from id3 import Id3Estimator
from id3 import export_graphviz

# remove utf-8, tira espaços, quebra por ','
def trata_linha(linha):
    vals = linha.replace("\"", "").replace("\n", "").replace("ã", "a").replace("ç", "c").replace("í", "i").replace("é", "e").replace("ó", "o").split(",")
    return [val.strip() for val in vals] 


# recebe a lista dos resultados das linhas com o valor [2 bolsonaro, 2 haddad, 2 ciro...]
# retorna a entropia do valor
def entropia(resultados):
    valores = resultados.values()
    total = sum(valores)
    entropia = 0.0
    for res in valores:
        if not (res == 0):
            entropia += -(res/total)*math.log(res/total, 2)
    return entropia

# recebe a entropia total da matriz, entropia dos valores do atributo, e quantidades dos valores na matriz
def ganho(entropia_total, entropias_valores, quanidades_valores):
    ganho = entropia_total
    for i in xrange(0,len(entropias_valores)):
        proporcao = quanidades_valores[i]/sum(quanidades_valores)
        if(proporcao!=0):
            ganho += -proporcao*math.log(proporcao, 2)*entropias_valores[i]
    return ganho


# recebe a matriz de respostas e a lista de colunas
# retorna um dict na seguinte estrutura:
# quantidades[atributo][valor_do_atributo] = qtd_respostas
def quantidades(matriz, colunas):
    totais = {col: totais_col(idx, matriz) for idx, col in enumerate(colunas)}
    for linha in matriz:
        for idx, val in enumerate(linha):
            totais[colunas[idx]][val] += 1
    return totais

# monta etrutura para somar as quantidades dos valores
def totais_col(idx, matriz):
    totais = []
    for linha in matriz:
        for i, valor in enumerate(linha):
            if i == idx and valor not in totais:
                totais.append(valor)
    return {val: 0.0 for val in totais}



# recebe a matriz de respostas, a lista de colunas e as quantidades totais
# returna [entropias, sub_matrizes]

# entropias tem a seguinte estrutura:
# entropias[atributo][valor_do_atributo] = entropia_valor_atributo

# sub_matrizes tem a seguinte estrutura:
# sub_matrizes[atributo][valor_do_atributo] = sub_matrizes_valor_atributo  (filtra a matriz)
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
                entropias[atributo][valor] = entropia(quantidades(sub_matrizes[atributo][valor], colunas)[colunas[-2]])
    return [entropias, sub_matrizes]


# ganhos dos atributos fora o resultado
def ganhos(entropias, totais, entropia_total):
    ganhos = {}
    for atributo in entropias.keys():
        if(atributo != 'voto'):
            entropias_valores = entropias[atributo].values()
            quanidades_valores = totais[atributo].values()
            ganhos[atributo] = ganho(entropia_total, entropias_valores, quanidades_valores)
    return ganhos

# folha da arvore
def resultado_formatado(lst):
        mais_comun = max(lst, key=lst.count)
        qtd = lst.count(mais_comun)
        return str((qtd*1.0)/len(lst)*100) + "% "+ mais_comun[0]

# calcula os nós da arvore recursivamente
# passando as submatrizes e subcolunas calculadas
def calcula_branch(matriz, colunas):
    if (len(colunas) == 1):
        return resultado_formatado(matriz)
    # if (len(matriz) == 1):
    #     return matriz
    totais = quantidades(matriz, colunas)
    resultados = totais['voto']
    entropia_total = entropia(resultados)
    ent_sub = entropias_e_sub_matrizes(matriz, colunas, totais)
    entropias = ent_sub[0]
    sub_matrizes = ent_sub[1]
    _ganhos = ganhos(entropias, totais, entropia_total)
    maior_ganho = max(_ganhos, key=_ganhos.get) # nome do atributo com maior ganho do nó
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

# print melhorado
def ap(s):
    pp.pprint(s)

pp = pprint.PrettyPrinter(indent=4)
file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]                         # coluna de atributos sem datahora
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:])) # matriz de respostas sem datahora
arvore = calcula_branch(matriz, colunas)
ap(arvore)


# TESTE
file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:]))
totais = quantidades(matriz, colunas)

valores = [attr.keys() for attr in totais.values()]
valores_i = [[{val: i} for i, val in enumerate(attr)] for attr in valores]
flat = [i for sublist in valores_i for i in sublist]
numero_do_valor = {}
numero_do_resultados = {res: i for i, res in enumerate(totais['voto'].keys())}
for d in flat:
    numero_do_valor.update(d)

data = [] 
for linha in matriz:
    sub_data = []
    for i, val in enumerate(linha):
        if i != colunas.index('voto'):
             sub_data.append(numero_do_valor[val])
    data.append(sub_data)

target = []
for linha in matriz: 
    for i, resultado in enumerate(linha):
        if i == colunas.index('voto'):
            target.append(numero_do_resultados[resultado])

bunch = load_breast_cancer()
estimator = Id3Estimator()
estimator.fit(data[:-1],target)
colunas.remove('voto')
export_graphviz(estimator.tree_, 'tree.dot', colunas)


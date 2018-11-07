# -*- coding: utf-8 -*-

import math

def trata_linha(linha):
    return linha.replace("\"", "").split(",")

def dados_col(idx, matriz):
    dados = []
    for linha in matriz:
        for i, valor in enumerate(linha):
            if i == idx and valor not in dados:
                dados.append(valor)
    return {val: 0.0 for val in dados}

def entropia(resultados):
    valores = resultados.values()
    total = sum(valores)
    return map(lambda x: -(x/total)*math.log(x/total, 2), valores)



file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:]))
dados = {col: dados_col(idx, matriz) for idx, col in enumerate(colunas)}
for linha in matriz:
    for idx, val in enumerate(linha):
        dados[colunas[idx]][val] += 1

resultados = dados[colunas[-2]]
entropia_total = entropia(resultados)
# outras_colunas = {k: v for k, v in dados.items() if not k.startswith('7-')}



# for k, v in outras_colunas.items():
#     print entropia(v)
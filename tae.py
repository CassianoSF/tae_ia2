# -*- coding: utf-8 -*-
import pprint
import math
pp = pprint.PrettyPrinter(indent=4)


def trata_linha(linha):
    return linha.replace("\"", "").replace("ã", "a").replace("ç", "c").replace("í", "i").replace("é", "e").replace("ó", "o").split(",")

file = open('data', 'rb')
linhas = file.readlines()
colunas = trata_linha(linhas[0])[1:]
matriz = list(map(lambda x: trata_linha(x)[1:], linhas[1:]))
coluna_alvo = 6

def entropia(x, total):
    print(x)
    print(total)
    if (x == 0 or x == total):
       return 0
    return -(x/total)*math.log(x/total, 2)-((total-x)/total)*math.log((total-x)/total, 2) 

def possiveis_resultados(matriz, coluna_alvo):
    possiveis_resultados = []
    for linha in matriz:
        for i, valor in enumerate(linha):
            if i == coluna_alvo and valor not in possiveis_resultados:
                possiveis_resultados.append(valor)
    return possiveis_resultados

def arvore(matriz, colunas, coluna_alvo):
    arvore = {}
    for resultado in possiveis_resultados(matriz, coluna_alvo):
        arvore[resultado] = {}
        for linha in matriz:
            for i, valor in enumerate(linha):
                if (i != coluna_alvo):
                    if (colunas[i] not in arvore[resultado].keys()):
                        arvore[resultado][colunas[i]] = {val: {"sims": 0, "naos": 0, "entropia": None, "matriz": []} for val in possiveis_resultados(matriz, i)}
                    if (linha[coluna_alvo] == resultado):
                        arvore[resultado][colunas[i]][valor]["sims"] += 1
                    else:
                        arvore[resultado][colunas[i]][valor]["naos"] += 1
    for resultado in arvore.keys():
        for coluna in arvore[resultado].keys():
            for valor in arvore[resultado][coluna].keys():
                node = arvore[resultado][coluna][valor]
                total = node['sims'] + node['naos']
                node['entropia'] = entropia(node['sims'], total)
    return arvore


pp.pprint(arvore(matriz, colunas, coluna_alvo))


# def dados_col(idx, matriz):
#     dados = []
#     for linha in matriz:
#         for i, valor in enumerate(linha):
#             if i == idx and valor not in dados:
#                 dados.append(valor)
#     return {val: 0.0 for val in dados}

# def entropias(valores):
#     total = sum(valores)
#     return map(lambda x: entropia(x, total), valores)


# # coluna_alvo = colunas[0:coluna_alvo-1]+colunas[coluna_alvo+1:len(matriz)]
# # matriz_alvo = list(map(lambda x: x[0:coluna_alvo-1]+x[coluna_alvo+1:len(matriz)], matriz))

# dados = {col: dados_col(idx, matriz) for idx, col in enumerate(colunas)}
# for linha in matriz:
#     for idx, val in enumerate(linha):
#         dados[colunas[idx]][val] += 1

# resultados = dados[colunas[-2]]
# dados = {k: v for k, v in dados.items() if not k.startswith('7_')}
# valores = resultados.values()
# entropias_totais = entropias(valores)

# total = sum(resultados.values())




# for resultado, votos in resultados.items():
#     for idx_col, atributo in enumerate(colunas):
#         sims = filter(lambda linha: (linha[idx]) ,matriz)
    
#     entropia(votos, total) - (votos/total) 



# def ganho(entropia_total, total, ):
#     for val, qtd in qtd_valores.items():
        

# for entropia in entropias_totais:
#     for col, qtd_valores in dados.items():
#         ganho(entropia, qtd_valores, matriz)
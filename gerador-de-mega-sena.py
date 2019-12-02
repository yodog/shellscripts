#!/usr/bin/env python

from ast import literal_eval
from pprint import pprint

import math
import random
import sys

__author__  = 'RASG'
__version__ = '2019.12.02.1753'

# funcao que calcula o preco dos jogos da mega-sena (individual, total)
def preco(n,d):
    p = 4.50
    f = math.factorial(d) / (math.factorial(6) * math.factorial(d - 6))
    i = p * f
    t = i * n
    return (i, t)


# funcao que cria os jogos
def jogar(lista):
    global jogos, universo, valortotal
    jogo = []

    print 'lista de jogos do usuario:', lista
    print

    # iterar lista de tuplas
    for tupla in lista:
        tupla = literal_eval(tupla)
        n,d = tupla

        ci,ct = preco(n,d)
        valortotal += ct

        print 'universo tem', len(universo), 'numeros disponiveis'
        print 'gerando', n, 'jogo(s) de', d, 'dezenas'
        print 'custo', 'individual:', ci, 'total:', ct
        print

        # iterar quantidade de jogos solicitados
        for j in range(0, n):

            # se nao tivermos a quantidade de numeros necessarios no universo
            # usar os que ainda temos
            # definir novamente o universo com os numeros 1 a 60
            # preencher os numeros que faltavam no jogo com uma amostra aleatoria
            if len(universo) < d:
                print 'universo nao tem numeros disponiveis para o proximo jogo'
                print 'adicionando numeros ao universo'
                print

                jogo = universo
                universo = range(1, 61)
                jogo += random.sample(universo, (d - len(jogo)))

            # se tivermos a quantidade de numeros necessarios no universo
            # pegar uma amostra aleatoria
            else:
                jogo = sorted(random.sample(universo, d))

            # retirar do universo os numeros usados
            universo = [e for e in universo if e not in jogo]

            # adicionar o jogo na lista de jogos
            jogos.append(jogo)

# numeros disponveis (1 a 60)
universo = range(1, 61)

# lista de jogos que sera impressa no final
jogos = []

# valor total gasto com os jogos
valortotal = 0

# argumentos passados para este script
scriptname = sys.argv[0]
argumentos = sys.argv[1:]

# chamar funcao com os argumentos passados pelo usuario
jogar(argumentos)

# contar elementos recursivamente sem repetir
ne = len(set(x for l in jogos for x in l))

# imprimir informacoes de execucao do script
print 'fim do script'
#print 'universo tem', len(universo), 'numeros disponiveis'
print 'foram usados', ne, 'numeros diferentes'
print 'valor total dos jogos:', valortotal
print

# imprimir os jogos
print
pprint([[str(i).zfill(2) for i in item] for item in jogos])
print

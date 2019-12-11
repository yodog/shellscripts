#!/usr/bin/env python

# Requires:
# pip install sortedcontainers

from ast import literal_eval
from pprint import pprint
from sortedcontainers import SortedSet

import math
import random
import sys

__author__  = 'RASG'
__version__ = '2019.12.11.1357'

# calcula o preco dos jogos da mega-sena (individual, total)
def preco(n, d):
    p = 4.50
    f = math.factorial(d) / (math.factorial(6) * math.factorial(d - 6))
    i = p * f
    t = i * n
    return (i, t)

# calcula cota de bolao
def bolao(valortotal, numparticipantes):
    cotaminima = 5.00
    cota = round(valortotal / numparticipantes, 2)
    if cota < cotaminima:
        print '! atencao ! valor da cota (', cota, ') inferior ao minimo permitido pela caixa (', cotaminima, ')'
        sys.exit()
    return cota

# cria os jogos
def jogar(lista):
    global jogos, universo, valortotal, valorporjogador

    print
    print 'lista de jogos do usuario:', lista
    print

    # iterar lista de tuplas
    for tupla in lista:

        # tratar argumentos do script e transformar cada string em uma lista
        # adicionar o terceiro elemento (cotas) se nao for passado pelo usuario
        # e dividir em tres variaveis
        t = list(literal_eval(tupla))
        if (len(t) < 3): t.append(1)
        print t
        n,d,c = t

        # mega sena aceita no maximo 15 dezenas
        if d > 15:
            print 'numero de dezenas nao pode ser maior que 15'
            print
            sys.exit()

        # calcular precos
        ci,ct = preco(n,d)
        cb    = bolao(ct,c)
        valortotal += ct

        print 'universo tem', len(universo), 'numeros disponiveis'
        print 'gerando', n, 'jogo(s) de', d, 'dezenas dividido(s) em', c, 'cota(s)'
        print 'custo', 'individual:', ci, '| total:', ct, '| cota bolao:', cb
        print

        # iterar quantidade de jogos solicitados
        for j in range(0, n):

            # se nao tivermos a quantidade de numeros necessarios no universo
            # usar os que ainda temos
            # definir novamente o universo com os numeros 1 a 60
            # preencher os numeros que faltavam no jogo com uma amostra aleatoria
            if len(universo) < d:
                print 'universo tem', len(universo), 'numeros disponiveis mas precisamos de', d
                print 'adicionando numeros ao universo'
                print

                jogo = SortedSet(universo)
                universo = range(1, 61)

                while len(jogo) < d:
                    jogo.update(random.sample(universo, (d - len(jogo))))

            # se tivermos a quantidade de numeros necessarios no universo
            # pegar uma amostra aleatoria
            else:
                jogo = SortedSet(random.sample(universo, d))

            # retirar do universo os numeros usados
            universo = [e for e in universo if e not in jogo]

            # adicionar o jogo na lista de jogos
            jogos.append(jogo)

    valorporjogador = valortotal / c


# argumentos passados para este script
scriptname = sys.argv[0]
argumentos = sys.argv[1:]

# numeros disponveis (1 a 60)
universo = range(1, 61)

# lista de jogos que sera impressa no final
jogos = []

# valores que serao gastos com os jogos
valorporjogador = 0
valortotal      = 0

# chamar funcao com os argumentos passados pelo usuario
jogar(argumentos)

# contar recursivamente quantas dezenas foram usadas para montar os jogos
elemjogos  = [x for l in jogos for x in l]
numelems   = len(elemjogos)
semrepetir = len(set(elemjogos))

# imprimir informacoes de execucao do script
print 'fim do script'
print 'foram usados', semrepetir, 'numeros diferentes |', numelems, 'numeros no total'
print 'valor total dos jogos:', valortotal, '| por jogador:', valorporjogador

# imprimir os jogos
#impresso = [[str(i).zfill(2) for i in item] for item in jogos]
impresso = [' '.join([str(i).zfill(2) for i in item]) for item in jogos]

print
print 'jogos na ordem definida pelo usuario'
print
pprint(impresso)

print
print 'jogos em ordem crescente'
print
pprint(sorted(impresso))
print

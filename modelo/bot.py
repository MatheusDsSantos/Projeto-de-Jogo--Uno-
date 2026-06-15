"""
BOT - a "inteligencia" dos jogadores controlados pelo computador.

A estrategia e simples:
1. Entre as cartas validas, prefere jogar uma carta comum (guarda os
   curingas para quando nao tiver outra opcao).
2. Ao jogar um curinga, escolhe a cor que mais aparece na propria mao.
"""

import random

from modelo.carta import Carta
from modelo.jogo import JogoUno


def escolher_jogada(jogo, jogador):
    """
    Decide a jogada do bot.
    Retorna (indice, cor_escolhida):
      - indice: posicao da carta na mao, ou None se for comprar
      - cor_escolhida: cor para o curinga, ou None se nao for curinga
    """
    indices_validos = jogo.cartas_validas(jogador)
    if not indices_validos:
        return None, None  # Sem carta valida: vai comprar

    cartas = jogador.cartas()

    # Prefere cartas comuns; curingas ficam como ultima opcao
    indices_comuns = [i for i in indices_validos if cartas[i].cor != "Curinga"]
    if indices_comuns:
        indice = random.choice(indices_comuns)
    else:
        indice = random.choice(indices_validos)

    cor_escolhida = None
    if cartas[indice].cor == "Curinga":
        cor_escolhida = _cor_mais_frequente(cartas)

    return indice, cor_escolhida


def _cor_mais_frequente(cartas):
    """Retorna a cor que mais aparece na mao (ignorando curingas)."""
    contagem = {cor: 0 for cor in JogoUno.CORES}
    for carta in cartas:
        if carta.cor in contagem:
            contagem[carta.cor] += 1

    melhor_cor = max(contagem, key=contagem.get)
    if contagem[melhor_cor] == 0:
        return random.choice(JogoUno.CORES)
    return melhor_cor

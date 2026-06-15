"""
Pacote com o modelo do jogo UNO:

- Carta: representa uma carta e suas regras de combinacao
- Jogador: um jogador e sua mao de cartas (lista encadeada)
- JogoUno: o motor do jogo (regras, turnos, efeitos), sem entrada/saida,
  para poder ser usado tanto pelo terminal quanto pelo servidor web
- bot: a "inteligencia" dos jogadores controlados pelo computador
"""

from modelo.carta import Carta
from modelo.jogador import Jogador
from modelo.jogo import JogoUno

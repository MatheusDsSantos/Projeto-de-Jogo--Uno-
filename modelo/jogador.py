"""
JOGADOR - um jogador do UNO e sua mao de cartas (lista encadeada).
"""

from estruturas.lista_encadeada import ListaEncadeada
from modelo.carta import Carta


class Jogador:
    """Representa um jogador do UNO."""

    def __init__(self, nome, eh_bot=False):
        self.nome = nome
        self.eh_bot = eh_bot         # True se for controlado pelo computador
        self.mao = ListaEncadeada()  # As cartas na mao (lista encadeada)

    def receber_carta(self, carta):
        """Adiciona uma carta na mao do jogador."""
        self.mao.adicionar(carta)

    def jogar_carta(self, indice):
        """Remove e retorna a carta escolhida pelo jogador."""
        return self.mao.remover_por_indice(indice)

    def cartas(self):
        """Retorna as cartas da mao como lista Python."""
        return self.mao.listar()

    def tem_carta_valida(self, carta_do_topo, cor_atual):
        """Verifica se o jogador tem alguma carta que pode jogar."""
        carta_referencia = Carta(cor_atual, carta_do_topo.valor)
        for carta in self.mao.listar():
            if carta.pode_jogar_sobre(carta_referencia):
                return True
        return False

    def quantidade_cartas(self):
        return self.mao.tamanho

    def sem_cartas(self):
        return self.mao.esta_vazia()

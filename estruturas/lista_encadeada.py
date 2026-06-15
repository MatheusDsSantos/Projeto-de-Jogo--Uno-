"""
LISTA ENCADEADA - usada para guardar as cartas da mao de cada jogador.
"""


class No:
    """Um no da lista encadeada. Guarda uma carta e aponta para o proximo."""

    def __init__(self, carta):
        self.carta = carta
        self.proximo = None  # Aponta para o proximo no


class ListaEncadeada:
    """Lista encadeada para guardar as cartas de um jogador."""

    def __init__(self):
        self.inicio = None  # Primeiro no da lista
        self.tamanho = 0

    def adicionar(self, carta):
        """Adiciona uma carta no final da lista."""
        novo_no = No(carta)

        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no

        self.tamanho += 1

    def remover_por_indice(self, indice):
        """Remove e retorna a carta na posicao indicada."""
        if self.inicio is None or indice < 0 or indice >= self.tamanho:
            return None

        if indice == 0:
            carta = self.inicio.carta
            self.inicio = self.inicio.proximo
            self.tamanho -= 1
            return carta

        atual = self.inicio
        for _ in range(indice - 1):
            atual = atual.proximo

        carta = atual.proximo.carta
        atual.proximo = atual.proximo.proximo
        self.tamanho -= 1
        return carta

    def listar(self):
        """Retorna todas as cartas como uma lista Python (para exibir)."""
        cartas = []
        atual = self.inicio
        while atual is not None:
            cartas.append(atual.carta)
            atual = atual.proximo
        return cartas

    def esta_vazia(self):
        return self.tamanho == 0

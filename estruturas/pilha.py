"""
PILHA (Stack) - usada para o monte de compra e o monte de descarte.
Funciona como LIFO: ultimo a entrar, primeiro a sair.
"""

import random


class Pilha:
    """Pilha (Stack) - funciona como LIFO: ultimo a entrar, primeiro a sair."""

    def __init__(self):
        self._cartas = []

    def empurrar(self, carta):
        """Coloca uma carta no topo da pilha."""
        self._cartas.append(carta)

    def retirar(self):
        """Remove e retorna a carta do topo da pilha."""
        if self.esta_vazia():
            return None
        return self._cartas.pop()

    def ver_topo(self):
        """Olha a carta do topo sem remover."""
        if self.esta_vazia():
            return None
        return self._cartas[-1]

    def esta_vazia(self):
        return len(self._cartas) == 0

    def tamanho(self):
        return len(self._cartas)

    def embaralhar(self):
        random.shuffle(self._cartas)

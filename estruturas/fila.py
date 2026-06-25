"""
FILA (Queue) - usada para controlar a ordem dos turnos dos jogadores.
Funciona como FIFO: primeiro a entrar, primeiro a sair.
"""
# deque = "double-ended queue": tipo uma lista, mas otimizada pra
# inserir/remover nos dois extremos em O(1). Usada aqui porque a Fila
# remove sempre do início (popleft), o que numa list normal seria O(n).


from collections import deque


class Fila:
    """Fila funciona como FIFO: primeiro a entrar, primeiro a sair."""

    def __init__(self):
        self._jogadores = deque()

    def entrar(self, jogador):
        """Adiciona um jogador no final da fila."""
        self._jogadores.append(jogador)

    def proximo(self):
        """Remove e retorna o primeiro jogador da fila."""
        if self.esta_vazia():
            return None
        return self._jogadores.popleft()

    def ver_primeiro(self):
        """Olha quem e o primeiro sem remover."""
        if self.esta_vazia():
            return None
        return self._jogadores[0]

    def inverter(self):
        """Inverte a ordem da fila (efeito da carta Inverter)."""
        self._jogadores = deque(reversed(self._jogadores))

    def listar(self):
        """Retorna os jogadores como lista Python (sem alterar a fila)."""
        return list(self._jogadores)

    def esta_vazia(self):
        return len(self._jogadores) == 0

    def quantidade(self):
        return len(self._jogadores)

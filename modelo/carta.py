"""
CARTA - representa uma carta do UNO e a regra de quando pode ser jogada.
"""


class Carta:
    """Representa uma carta do UNO."""

    def __init__(self, cor, valor):
        self.cor = cor      # Ex: "Vermelho", "Azul", "Curinga"
        self.valor = valor  # Ex: "5", "Pular", "+2", "Curinga", "+4"

    def __str__(self):
        if self.cor == "Curinga":
            return f"[{self.valor}]"
        return f"[{self.cor} {self.valor}]"

    def pode_jogar_sobre(self, carta_do_topo):
        """Verifica se esta carta pode ser jogada sobre a carta do topo."""
        # Curingas sempre podem ser jogados
        if self.cor == "Curinga":
            return True
        # Mesma cor ou mesmo valor
        if self.cor == carta_do_topo.cor:
            return True
        if self.valor == carta_do_topo.valor:
            return True
        return False

    def para_dicionario(self):
        """Converte a carta para dicionario (usado pela API web em JSON)."""
        return {"cor": self.cor, "valor": self.valor}

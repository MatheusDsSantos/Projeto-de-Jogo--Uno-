"""
JOGO UNO - o motor do jogo.

Esta classe contem TODAS as regras do UNO, mas nao usa input() nem print().
Quem conversa com o usuario e a interface (terminal ou web). Assim o mesmo
motor funciona nos dois lugares.

Estruturas de dados usadas:
- Pilha: monte de compra e monte de descarte
- Fila: ordem dos turnos dos jogadores
- Lista Encadeada: mao de cada jogador (dentro de Jogador)
- Arvore Binaria de Busca: ranking dos jogadores (metodo ranking())
"""

import random

from estruturas.pilha import Pilha
from estruturas.fila import Fila
from estruturas.arvore import ArvoreBinariaBusca
from modelo.carta import Carta
from modelo.jogador import Jogador


class JogoUno:
    """Controla toda a logica do jogo UNO."""

    CORES = ["Vermelho", "Azul", "Verde", "Amarelo"]
    VALORES_NORMAIS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    VALORES_ESPECIAIS = ["Pular", "Inverter", "+2"]

    def __init__(self, jogadores):
        """
        jogadores: lista de objetos Jogador ja criados
                   (a interface decide quem e humano e quem e bot).
        """
        self.monte_compra = Pilha()
        self.monte_descarte = Pilha()
        self.fila_jogadores = Fila()
        self.cor_atual = None    # Cor valida para jogadas (muda com curinga)
        self.vencedor = None     # Recebe o Jogador que ganhar
        self.log = []            # Historico de mensagens do jogo

        self._criar_baralho()
        for jogador in jogadores:
            self.fila_jogadores.entrar(jogador)
        self._distribuir_cartas()
        self._virar_primeira_carta()

    # --------------------------------------------------------
    # PREPARACAO DO JOGO
    # --------------------------------------------------------

    def _criar_baralho(self):
        """Cria e embaralha todas as 108 cartas do UNO."""
        cartas = []

        for cor in self.CORES:
            # Cada cor tem: 1x zero, 2x de cada numero (1-9), 2x de cada especial
            cartas.append(Carta(cor, "0"))
            for valor in self.VALORES_NORMAIS[1:]:
                cartas.append(Carta(cor, valor))
                cartas.append(Carta(cor, valor))
            for especial in self.VALORES_ESPECIAIS:
                cartas.append(Carta(cor, especial))
                cartas.append(Carta(cor, especial))

        # 4 curingas normais e 4 curingas +4
        for _ in range(4):
            cartas.append(Carta("Curinga", "Curinga"))
            cartas.append(Carta("Curinga", "+4"))

        # Embaralha e coloca tudo na pilha de compra
        random.shuffle(cartas)
        for carta in cartas:
            self.monte_compra.empurrar(carta)

    def _distribuir_cartas(self):
        """Da 7 cartas para cada jogador."""
        for _ in range(7):
            for jogador in self.fila_jogadores.listar():
                jogador.receber_carta(self.monte_compra.retirar())

    def _virar_primeira_carta(self):
        """Retira a primeira carta do monte para iniciar o descarte."""
        while True:
            carta = self.monte_compra.retirar()
            # A primeira carta nao pode ser curinga
            if carta.cor != "Curinga":
                self.monte_descarte.empurrar(carta)
                self.cor_atual = carta.cor
                break
            else:
                self.monte_compra.empurrar(carta)
                self.monte_compra.embaralhar()

    # --------------------------------------------------------
    # CONSULTAS (nao alteram o estado do jogo)
    # --------------------------------------------------------

    def jogador_da_vez(self):
        """Retorna o jogador no inicio da fila (sem remover)."""
        return self.fila_jogadores.ver_primeiro()

    def carta_do_topo(self):
        """Retorna a carta visivel no topo do descarte."""
        return self.monte_descarte.ver_topo()

    def acabou(self):
        return self.vencedor is not None

    def cartas_validas(self, jogador):
        """Retorna os indices das cartas da mao que podem ser jogadas agora."""
        topo = self.carta_do_topo()
        referencia = Carta(self.cor_atual, topo.valor)
        indices = []
        for i, carta in enumerate(jogador.cartas()):
            if carta.pode_jogar_sobre(referencia):
                indices.append(i)
        return indices

    def ranking(self):
        """
        Monta o RANKING usando uma ARVORE BINARIA DE BUSCA.

        Cada jogador e inserido na arvore tendo como chave a quantidade
        de cartas na mao. O percurso EM ORDEM devolve os jogadores ja
        ordenados: quem tem menos cartas (esta ganhando) aparece primeiro.
        """
        arvore = ArvoreBinariaBusca()
        for jogador in self.fila_jogadores.listar():
            arvore.inserir(jogador.quantidade_cartas(), jogador.nome)
        if self.vencedor is not None:
            arvore.inserir(0, self.vencedor.nome)

        return [
            {"nome": nome, "cartas": quantidade}
            for quantidade, nome in arvore.em_ordem()
        ]

    # --------------------------------------------------------
    # ACOES (alteram o estado do jogo)
    # --------------------------------------------------------

    def registrar(self, mensagem):
        """Guarda uma mensagem no historico do jogo."""
        self.log.append(mensagem)

    def jogar_carta(self, indice, cor_escolhida=None):
        """
        O jogador da vez joga a carta na posicao 'indice' da mao.
        Se a carta for curinga, 'cor_escolhida' deve ser uma das CORES.
        Levanta ValueError se a jogada for invalida.
        Retorna a carta jogada.
        """
        if self.acabou():
            raise ValueError("O jogo ja terminou.")

        jogador = self.jogador_da_vez()
        cartas = jogador.cartas()

        if indice < 0 or indice >= len(cartas):
            raise ValueError("Numero de carta invalido.")

        carta = cartas[indice]
        topo = self.carta_do_topo()
        referencia = Carta(self.cor_atual, topo.valor)

        if not carta.pode_jogar_sobre(referencia):
            raise ValueError(f"A carta {carta} nao pode ser jogada agora.")

        if carta.cor == "Curinga" and cor_escolhida not in self.CORES:
            raise ValueError("Escolha uma cor para o curinga.")

        # Jogada valida: remove a carta da mao e coloca no descarte
        self.fila_jogadores.proximo()  # Retira o jogador da frente da fila
        carta_jogada = jogador.jogar_carta(indice)
        self.monte_descarte.empurrar(carta_jogada)
        self.registrar(f"{jogador.nome} jogou {carta_jogada}")

        # Atualiza a cor atual
        if carta_jogada.cor == "Curinga":
            self.cor_atual = cor_escolhida
            self.registrar(f"{jogador.nome} escolheu a cor {cor_escolhida}")
        else:
            self.cor_atual = carta_jogada.cor

        # Aviso de UNO
        if jogador.quantidade_cartas() == 1:
            self.registrar(f"*** {jogador.nome} gritou UNO! ***")

        # Verifica vitoria
        if jogador.sem_cartas():
            self.vencedor = jogador
            self.registrar(f"{jogador.nome} venceu o jogo!")
            return carta_jogada

        # O efeito Inverter atua na fila ANTES do jogador voltar para o
        # final, para que a ordem dos outros jogadores fique invertida
        if carta_jogada.valor == "Inverter":
            self.fila_jogadores.inverter()
            self.registrar("A ordem dos jogadores foi INVERTIDA!")

        # Devolve o jogador para o final da fila
        self.fila_jogadores.entrar(jogador)

        # Efeitos que pulam o proximo jogador
        if carta_jogada.valor in ("Pular", "+2", "+4"):
            self._aplicar_efeito_no_proximo(carta_jogada)

        return carta_jogada

    def comprar_e_passar(self):
        """O jogador da vez compra 1 carta e passa o turno."""
        if self.acabou():
            raise ValueError("O jogo ja terminou.")

        jogador = self.fila_jogadores.proximo()
        self._comprar_carta(jogador, 1)
        self.fila_jogadores.entrar(jogador)

    def _aplicar_efeito_no_proximo(self, carta):
        """Aplica Pular, +2 ou +4 no proximo jogador da fila."""
        proximo = self.fila_jogadores.proximo()

        if carta.valor == "+2":
            self._comprar_carta(proximo, 2)
        elif carta.valor == "+4":
            self._comprar_carta(proximo, 4)

        self.registrar(f"{proximo.nome} foi PULADO!")
        # Devolve o jogador pulado ao final da fila sem jogar
        self.fila_jogadores.entrar(proximo)

    def _comprar_carta(self, jogador, quantidade=1):
        """Faz o jogador comprar cartas do monte."""
        compradas = 0
        for _ in range(quantidade):
            # Se o monte acabar, recicla o descarte
            if self.monte_compra.esta_vazia():
                self._reciclar_descarte()
            carta = self.monte_compra.retirar()
            if carta:
                jogador.receber_carta(carta)
                compradas += 1
        if compradas > 0:
            plural = "carta" if compradas == 1 else "cartas"
            self.registrar(f"{jogador.nome} comprou {compradas} {plural}")

    def _reciclar_descarte(self):
        """Move as cartas do descarte de volta para o monte de compra."""
        if self.monte_descarte.tamanho() <= 1:
            return  # Nao ha cartas suficientes para reciclar
        self.registrar("Reciclando o monte de compra...")
        topo = self.monte_descarte.retirar()  # Guarda a carta do topo
        while not self.monte_descarte.esta_vazia():
            self.monte_compra.empurrar(self.monte_descarte.retirar())
        self.monte_compra.embaralhar()
        self.monte_descarte.empurrar(topo)  # Devolve o topo

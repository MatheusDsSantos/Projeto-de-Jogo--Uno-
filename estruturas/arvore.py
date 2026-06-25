


class NoArvore:
    """Um no da arvore binaria de busca."""

    def __init__(self, chave, valor):
        self.chave = chave        # quantidade de cartas do jogador
        self.valor = valor        # nome do jogador
        self.esquerda = None      # filho com chave menor
        self.direita = None       # filho com chave maior ou igual


class ArvoreBinariaBusca:
    """Arvore Binaria de Busca para ordenar os jogadores no ranking."""

    def __init__(self):
        self.raiz = None

    def inserir(self, chave, valor):
        """Insere um par (chave, valor) na posicao correta da arvore."""
        novo = NoArvore(chave, valor)

        if self.raiz is None:
            self.raiz = novo
            return

        atual = self.raiz
        while True:
            if chave < atual.chave:
                # Chave menor: vai para a esquerda
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return
                atual = atual.esquerda
            else:
                # Chave maior ou igual: vai para a direita
                if atual.direita is None:
                    atual.direita = novo
                    return
                atual = atual.direita

    def em_ordem(self):
    
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _em_ordem_recursivo(self, no, resultado):
        if no is None:
            return
        self._em_ordem_recursivo(no.esquerda, resultado)
        resultado.append((no.chave, no.valor))
        self._em_ordem_recursivo(no.direita, resultado)

    def buscar(self, chave):
        """Busca um no pela chave. Retorna o valor ou None se nao existir."""
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual.valor
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def altura(self):
        """Retorna a altura da arvore (0 para arvore vazia)."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, no):
        if no is None:
            return 0
        altura_esq = self._altura_recursiva(no.esquerda)
        altura_dir = self._altura_recursiva(no.direita)
        return 1 + max(altura_esq, altura_dir)

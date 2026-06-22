# Estrutura de Dados `ArvoreBinariaBusca` (e `NoArvore`)

## Objetivo

Ordenar os jogadores por quantidade de cartas na mão, sem usar `sort()`, através do percurso em ordem de uma árvore binária de busca.

## Responsabilidades

- `NoArvore`: guardar uma chave (quantidade de cartas), um valor (nome do jogador) e os filhos `esquerda`/`direita`.
- `ArvoreBinariaBusca`: inserir nós respeitando a propriedade da ABB e percorrer a árvore em ordem para gerar o ranking.

## Papel no Fluxo

A árvore é criada e descartada **dentro** de `JogoUno.ranking()` — não é um atributo guardado entre jogadas. A cada chamada, uma árvore nova é montada do zero com o estado atual dos jogadores.

| Situação | Exemplo |
|---|---|
| Jogador A tem 3 cartas, Jogador B tem 7, Bot C tem 1 | `inserir(3, "A")`, `inserir(7, "B")`, `inserir(1, "C")` |
| Resultado de `em_ordem()` | `[(1, "C"), (3, "A"), (7, "B")]` — do que tem menos para o que tem mais |

Regra de inserção: chave **menor** vai para a subárvore **esquerda**; chave **maior ou igual** vai para a subárvore **direita**.

## Atributos / Estado

```python
class NoArvore:
    chave: int       # quantidade de cartas do jogador
    valor: str        # nome do jogador
    esquerda: NoArvore | None
    direita: NoArvore | None

class ArvoreBinariaBusca:
    raiz: NoArvore | None
```

## Métodos / Funções

```python
def inserir(self, chave, valor) -> None
def em_ordem(self) -> list[tuple]
def buscar(self, chave) -> str | None
def altura(self) -> int
```

## Validações

- Não há validação de chaves duplicadas: jogadores com a mesma quantidade de cartas convivem na árvore (uma vai para a subárvore direita da outra, pela regra "maior ou igual").

## Não Deve Fazer

- Não remove nós (não existe `remover`) — a árvore é sempre reconstruída a cada chamada de `ranking()`, então remoção não é necessária.
- Não se autobalanceia — não é uma AVL nem Rubro-Negra. O método `altura()` existe para inspecionar esse desequilíbrio, mas não é usado pela interface.

## Exemplo de Uso

```python
arvore = ArvoreBinariaBusca()
arvore.inserir(3, "Matheus")
arvore.inserir(1, "Bot Ana")
arvore.inserir(7, "Bot Beto")

arvore.em_ordem()
# [(1, "Bot Ana"), (3, "Matheus"), (7, "Bot Beto")]
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — método `ranking()`, único ponto que usa esta estrutura.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN13 (montagem do ranking).
- [Diagrama de Arquitetura](../arquitetura/diagrama.md) — relação de uso entre `JogoUno` e `ArvoreBinariaBusca`.

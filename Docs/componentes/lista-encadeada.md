# Estrutura de Dados `ListaEncadeada` (e `No`)

## Objetivo

Guardar as cartas da mão de um jogador como uma cadeia de nós, em vez de um array com posições fixas.

## Responsabilidades

- `No`: guardar uma `Carta` e uma referência (`proximo`) para o nó seguinte.
- `ListaEncadeada`: manter o ponteiro `inicio`, o `tamanho` da lista, e oferecer operações de inserir, remover e listar percorrendo a cadeia.

## Papel no Fluxo

`ListaEncadeada` é o atributo `mao` dentro de [`Jogador`](jogador.md) — cada jogador tem a sua própria instância.

| Situação | Método chamado | Efeito |
|---|---|---|
| Jogador recebe uma carta (início ou compra) | `adicionar(carta)` | percorre até o último nó e encadeia um novo no final |
| Jogador joga uma carta da mão | `remover_por_indice(indice)` | percorre até a posição e reconecta a cadeia ao redor do nó removido |
| Exibir a mão (terminal ou web) | `listar()` | percorre todos os nós e devolve uma lista Python |
| Saber se o jogador venceu | `esta_vazia()` | verifica se `tamanho == 0` |

## Atributos / Estado

```python
class No:
    carta: Carta
    proximo: No | None

class ListaEncadeada:
    inicio: No | None
    tamanho: int
```

## Métodos / Funções

```python
# No não tem métodos, apenas os dois atributos acima.

def adicionar(self, carta) -> None
def remover_por_indice(self, indice) -> Carta | None
def listar(self) -> list
def esta_vazia(self) -> bool
```

## Validações

- `remover_por_indice` retorna `None` se `indice` for negativo, maior ou igual a `tamanho`, ou se a lista estiver vazia — não levanta exceção. A validação de "número de carta inválido" para o usuário é feita em [`JogoUno.jogar_carta`](jogo-uno.md).

## Não Deve Fazer

- Não sabe se uma carta pode ser jogada sobre outra — essa regra é de [`Carta.pode_jogar_sobre`](carta.md).
- Não tem acesso a outros jogadores nem ao estado da partida.

## Exemplo de Uso

```python
mao = ListaEncadeada()
mao.adicionar(Carta("Azul", "7"))
mao.adicionar(Carta("Curinga", "+4"))

carta_jogada = mao.remover_por_indice(0)  # remove a primeira carta
cartas_restantes = mao.listar()           # ["[Curinga +4]"]
```

## Links Relacionados

- [`Jogador`](jogador.md) — dono da lista encadeada (`mao`).
- [`Carta`](carta.md) — o que cada `No` guarda.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN02 (distribuição inicial), RN09 (compra de carta).

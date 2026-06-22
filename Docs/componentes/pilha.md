# Estrutura de Dados `Pilha`

## Objetivo

Armazenar cartas em ordem LIFO (Last In, First Out — último a entrar, primeiro a sair), usada no monte de compra e no monte de descarte.

## Responsabilidades

- Guardar uma coleção ordenada de `Carta`.
- Permitir colocar uma carta no topo (`empurrar`).
- Permitir retirar a carta do topo (`retirar`).
- Permitir consultar a carta do topo sem remover (`ver_topo`).
- Embaralhar a ordem das cartas internas.

## Papel no Fluxo

`Pilha` é usada duas vezes dentro de `JogoUno`: como `monte_compra` e como `monte_descarte`.

| Situação | Pilha usada | Método chamado |
|---|---|---|
| Jogador compra uma carta | `monte_compra` | `retirar()` |
| Jogador joga uma carta | `monte_descarte` | `empurrar(carta)` |
| Validar a jogada atual | `monte_descarte` | `ver_topo()` |
| Monte de compra esgota | `monte_compra` e `monte_descarte` | `embaralhar()` + `empurrar()` |

## Atributos / Estado

```python
class Pilha:
    _cartas: list  # lista Python usada internamente como pilha
```

## Métodos / Funções

```python
def empurrar(self, carta) -> None
def retirar(self) -> Carta | None
def ver_topo(self) -> Carta | None
def esta_vazia(self) -> bool
def tamanho(self) -> int
def embaralhar(self) -> None
```

## Validações

- `retirar()` e `ver_topo()` retornam `None` quando a pilha está vazia — não levantam exceção.

## Não Deve Fazer

- Não conhece regras do UNO (não sabe o que é "carta válida"). Isso é responsabilidade de [`Carta`](carta.md) e [`JogoUno`](jogo-uno.md).
- Não decide quando reciclar o descarte — isso é feito por `JogoUno._reciclar_descarte()`.

## Exemplo de Uso

```python
monte = Pilha()
monte.empurrar(Carta("Vermelho", "5"))
monte.embaralhar()
carta = monte.retirar()  # remove e retorna a carta do topo
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — quem cria e usa as duas pilhas do jogo.
- [`Carta`](carta.md) — o que circula dentro da pilha.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN01 (baralho), RN10 (reciclagem).

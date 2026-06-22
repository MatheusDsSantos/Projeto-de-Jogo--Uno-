# Estrutura de Dados `Fila`

## Objetivo

Controlar a ordem dos turnos dos jogadores em regime FIFO (First In, First Out — primeiro a entrar, primeiro a sair).

## Responsabilidades

- Guardar os jogadores em uma ordem de atendimento.
- Mover o jogador da frente para o fim quando o turno passa.
- Inverter a direção da fila quando a carta Inverter é jogada.
- Permitir listar os jogadores sem alterar a fila (usado pelo ranking e pela tela de oponentes).

## Papel no Fluxo

`Fila` é o atributo `fila_jogadores` dentro de [`JogoUno`](jogo-uno.md).

| Situação | Método chamado | Efeito |
|---|---|---|
| Início do jogo | `entrar(jogador)` | cada jogador entra na fila na ordem recebida |
| Consultar quem joga agora | `ver_primeiro()` | não remove ninguém |
| Jogador termina a jogada | `proximo()` + `entrar(jogador)` | sai da frente e volta para o fim |
| Carta Inverter jogada | `inverter()` | a ordem dos próximos jogadores se inverte |
| Carta Pular / +2 / +4 jogada | `proximo()` (sem `entrar` imediato) | o próximo jogador é retirado para receber o efeito |
| Montar ranking ou lista de oponentes | `listar()` | retorna todos sem alterar a fila |

## Atributos / Estado

```python
class Fila:
    _jogadores: collections.deque  # fila implementada com deque
```

## Métodos / Funções

```python
def entrar(self, jogador) -> None
def proximo(self) -> Jogador | None
def ver_primeiro(self) -> Jogador | None
def inverter(self) -> None
def listar(self) -> list
def esta_vazia(self) -> bool
def quantidade(self) -> int
```

## Validações

- `proximo()` e `ver_primeiro()` retornam `None` se a fila estiver vazia (situação que não ocorre em uma partida normal, já que sempre há jogadores).

## Não Deve Fazer

- Não decide os efeitos das cartas (Pular, Inverter, +2, +4) — apenas executa a movimentação solicitada por [`JogoUno`](jogo-uno.md).
- Não sabe quantas cartas cada jogador tem.

## Exemplo de Uso

```python
fila = Fila()
fila.entrar(jogador_1)
fila.entrar(jogador_2)

da_vez = fila.proximo()       # jogador_1 sai da frente
fila.entrar(da_vez)           # jogador_1 volta para o fim

fila.inverter()               # inverte a ordem dos próximos turnos
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — orquestra `entrar`/`proximo`/`inverter` a cada jogada.
- [`Jogador`](jogador.md) — o que circula dentro da fila.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN06 (Pular), RN07 (Inverter), RN08 (+2/+4).

# Componente de Domínio `Jogador`

## Objetivo

Representar um participante da partida (humano ou bot) e sua mão de cartas.

## Responsabilidades

- Guardar o `nome` e se é controlado pelo computador (`eh_bot`).
- Manter a mão de cartas em uma [`ListaEncadeada`](lista-encadeada.md).
- Receber cartas, jogar cartas e responder sobre o próprio estado (quantidade de cartas, se está sem cartas, se tem jogada válida).

## Papel no Fluxo

`Jogador` é criado pela interface (terminal ou servidor web) e passado para [`JogoUno`](jogo-uno.md), que o coloca na [`Fila`](fila.md) de turnos.

| Situação | Método chamado |
|---|---|
| Início do jogo: distribuir 7 cartas | `receber_carta(carta)` |
| Jogador compra carta (efeito ou turno) | `receber_carta(carta)` |
| Jogador joga uma carta da mão | `jogar_carta(indice)` |
| Verificar se o bot precisa comprar | `tem_carta_valida(carta_do_topo, cor_atual)` |
| Exibir quantidade de cartas no painel | `quantidade_cartas()` |
| Checar vitória | `sem_cartas()` |

## Atributos / Estado

```python
class Jogador:
    nome: str
    eh_bot: bool
    mao: ListaEncadeada
```

## Métodos / Funções

```python
def receber_carta(self, carta) -> None
def jogar_carta(self, indice) -> Carta | None
def cartas(self) -> list
def tem_carta_valida(self, carta_do_topo, cor_atual) -> bool
def quantidade_cartas(self) -> int
def sem_cartas(self) -> bool
```

## Validações

- `tem_carta_valida` monta uma `Carta` de referência com `cor_atual` (não a cor original da carta do topo) — isso é necessário porque, após um curinga, a cor válida pode ser diferente da cor da carta física no topo do descarte.

## Não Deve Fazer

- Não decide a ordem dos turnos — isso é responsabilidade da [`Fila`](fila.md) dentro de `JogoUno`.
- Não valida regras globais da partida (vencedor, efeitos de cartas especiais) — isso é de [`JogoUno`](jogo-uno.md).
- Não tem estratégia própria de jogada quando é bot — a decisão de qual carta jogar é do módulo [`bot`](bot.md), não do `Jogador`.

## Exemplo de Uso

```python
jogador = Jogador("Matheus")
jogador.receber_carta(Carta("Verde", "3"))

if jogador.tem_carta_valida(carta_topo, cor_atual):
    carta = jogador.jogar_carta(0)
```

## Links Relacionados

- [`ListaEncadeada`](lista-encadeada.md) — estrutura que guarda a mão.
- [`Fila`](fila.md) — estrutura que guarda a ordem de jogadores.
- [`JogoUno`](jogo-uno.md) — orquestra todos os jogadores da partida.
- [`bot`](bot.md) — decide a jogada quando `eh_bot` é `True`.

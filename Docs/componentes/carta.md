# Componente de Domínio `Carta`

## Objetivo

Representar uma carta do UNO e a regra de quando ela pode ser jogada sobre outra.

## Responsabilidades

- Guardar `cor` e `valor` da carta.
- Saber se pode ser jogada sobre a carta do topo do descarte (`pode_jogar_sobre`).
- Converter-se em dicionário para ser enviada como JSON pela API web (`para_dicionario`).
- Ter uma representação textual amigável (`__str__`), usada pelo terminal.

## Papel no Fluxo

`Carta` é o dado mais básico do jogo: circula entre as pilhas (`monte_compra`, `monte_descarte`) e a lista encadeada de cada jogador.

| Situação | Quem usa `Carta` | Como |
|---|---|---|
| Montagem do baralho | [`JogoUno._criar_baralho`](jogo-uno.md) | cria as 108 instâncias |
| Validar jogada | [`JogoUno.cartas_validas`](jogo-uno.md) | cria uma carta de referência e chama `pode_jogar_sobre` |
| Verificar se o bot tem jogada | [`Jogador.tem_carta_valida`](jogador.md) | mesma lógica, do ponto de vista do jogador |
| Enviar estado para o navegador | [`servidor.py`](servidor-web.md) | chama `para_dicionario()` em cada carta visível |

## Atributos / Estado

```python
class Carta:
    cor: str    # "Vermelho", "Azul", "Verde", "Amarelo" ou "Curinga"
    valor: str  # "0".."9", "Pular", "Inverter", "+2", "Curinga" ou "+4"
```

## Métodos / Funções

```python
def __str__(self) -> str
def pode_jogar_sobre(self, carta_do_topo) -> bool
def para_dicionario(self) -> dict
```

## Validações

- `pode_jogar_sobre` retorna `True` em três casos: a própria carta é Curinga, a cor é igual à da carta do topo, ou o valor é igual ao da carta do topo. Em qualquer outro caso, retorna `False`.

## Não Deve Fazer

- Não sabe em qual pilha ou mão está — é um objeto de valor, sem referência ao restante do jogo.
- Não decide efeitos de jogo (quem compra cartas, quem é pulado). Isso é responsabilidade de [`JogoUno`](jogo-uno.md).

## Exemplo de Uso

```python
topo = Carta("Vermelho", "5")
minha_carta = Carta("Vermelho", "9")

minha_carta.pode_jogar_sobre(topo)  # True (mesma cor)

curinga = Carta("Curinga", "+4")
curinga.pode_jogar_sobre(topo)      # True (curinga sempre pode)
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — cria e valida cartas a cada jogada.
- [`Jogador`](jogador.md) — guarda cartas na mão.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN01 (baralho), RN04 (combinação de cartas).

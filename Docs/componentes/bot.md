# Módulo `bot`

## Objetivo

Decidir a jogada dos jogadores controlados pelo computador.

## Responsabilidades

- Escolher qual carta jogar entre as opções válidas.
- Preferir cartas comuns e guardar curingas como último recurso.
- Escolher a cor ao jogar um curinga, com base na cor mais frequente na própria mão.
- Sinalizar que o bot deve comprar quando não há jogada válida.

## Papel no Fluxo

`bot` é um módulo de funções (não uma classe). É chamado pela interface (terminal ou servidor web) sempre que `jogador.eh_bot` é `True` e é a vez desse jogador.

| Situação | Função chamada | Retorno |
|---|---|---|
| É a vez de um bot | `escolher_jogada(jogo, jogador)` | `(indice, cor_escolhida)` |
| Bot não tem carta válida | `escolher_jogada` retorna | `(None, None)` → quem chamou deve usar `jogo.comprar_e_passar()` |
| Bot vai jogar um curinga | `_cor_mais_frequente(cartas)` (interno) | a cor mais comum na mão do bot |

## Métodos / Funções

```python
def escolher_jogada(jogo, jogador) -> tuple  # (indice | None, cor_escolhida | None)
def _cor_mais_frequente(cartas) -> str
```

## Validações

- Se nenhuma cor aparecer na mão (só restam curingas), `_cor_mais_frequente` sorteia uma cor aleatória entre `JogoUno.CORES`.

## Não Deve Fazer

- Não chama `jogo.jogar_carta` nem `jogo.comprar_e_passar` diretamente — apenas decide e retorna a decisão. Quem aplica a jogada é a interface (`acao_bot_jogar` no [servidor](servidor-web.md), ou o laço do [terminal](terminal-uno.md)).
- Não guarda estado entre jogadas — cada chamada a `escolher_jogada` é independente.

## Exemplo de Uso

```python
indice, cor = bot.escolher_jogada(jogo, jogador_bot)
if indice is None:
    jogo.comprar_e_passar()
else:
    jogo.jogar_carta(indice, cor)
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — fornece `cartas_validas` para a decisão do bot.
- [`Jogador`](jogador.md) — fornece a mão (`cartas()`) usada na decisão.
- [Regras de Negócio](../regras/regras-de-negocio.md) — RN14 (estratégia do bot).
- [Servidor Web](servidor-web.md) — rota `/api/bot-jogar`, que dispara `escolher_jogada`.

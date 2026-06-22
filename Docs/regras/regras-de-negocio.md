# Regras de Negócio

Todas as regras abaixo estão implementadas em [`JogoUno`](../componentes/jogo-uno.md), salvo quando indicado.

## RN01 — Composição do Baralho

O baralho tem 108 cartas, criadas em `JogoUno._criar_baralho()`.

| Tipo de carta | Quantidade por cor | Cores | Total |
|---|---|---|---|
| "0" | 1 | Vermelho, Azul, Verde, Amarelo | 4 |
| "1" a "9" | 2 cada | Vermelho, Azul, Verde, Amarelo | 72 |
| Pular, Inverter, "+2" | 2 cada | Vermelho, Azul, Verde, Amarelo | 24 |
| Curinga | 4 | Curinga | 4 |
| "+4" | 4 | Curinga | 4 |
| **Total** | | | **108** |

**Exemplo:** existem exatamente 2 cartas `[Vermelho Pular]` e exatamente 1 carta `[Azul 0]`.

**Fluxo resumido:** cria a lista de 108 cartas → embaralha com `random.shuffle` → empilha tudo em `monte_compra`.

## RN02 — Distribuição Inicial de Cartas

Cada jogador recebe 7 cartas no início da partida (`JogoUno._distribuir_cartas()`).

| Situação | Resultado esperado |
|---|---|
| Partida com 2 jogadores | 14 cartas distribuídas, 94 restam no `monte_compra` |
| Partida com 4 jogadores | 28 cartas distribuídas, 80 restam no `monte_compra` |

A distribuição é feita "rodada por rodada": uma carta para cada jogador, repetido 7 vezes — não 7 cartas de uma vez para o mesmo jogador.

## RN03 — Carta Inicial do Descarte

A primeira carta do `monte_descarte` não pode ser Curinga (`JogoUno._virar_primeira_carta()`).

| Carta retirada do monte | Ação |
|---|---|
| Cor normal (Vermelho/Azul/Verde/Amarelo) | Vai para o descarte; define `cor_atual` |
| Curinga ou "+4" | Volta para o monte de compra, que é embaralhado novamente; tenta de novo |

## RN04 — Validação de Jogada (Combinação de Cartas)

Uma carta só pode ser jogada sobre a carta do topo se (`Carta.pode_jogar_sobre`):

| Condição | Pode jogar? |
|---|---|
| A carta é Curinga | Sim, sempre |
| Mesma cor da carta do topo | Sim |
| Mesmo valor da carta do topo | Sim |
| Nenhuma das condições acima | Não |

**Exemplo:** com o topo `[Vermelho 7]`, a carta `[Azul 7]` pode ser jogada (mesmo valor); a carta `[Azul 3]` não pode.

> Importante: a comparação usa `cor_atual` (não a cor literal da carta no topo) como referência — ver RN05.

## RN05 — Escolha de Cor ao Jogar Curinga

Ao jogar uma carta `Curinga` ou `+4`, o jogador deve escolher uma cor válida (`JogoUno.jogar_carta`).

| Condição | Resultado |
|---|---|
| Cor escolhida está em `CORES` (Vermelho/Azul/Verde/Amarelo) | `cor_atual` passa a ser essa cor |
| Cor ausente ou inválida | `ValueError("Escolha uma cor para o curinga.")` |

Essa nova `cor_atual` é o que vale para validar a próxima jogada — não a cor física "Curinga" da carta.

## RN06 — Efeito da Carta Pular

Quando `Pular` é jogada, o próximo jogador da fila perde a vez (`JogoUno._aplicar_efeito_no_proximo`).

**Resumo do fluxo:** jogador joga `Pular` → jogador volta ao fim da fila → próximo jogador é retirado da fila e devolvido ao fim **sem jogar**.

## RN07 — Efeito da Carta Inverter

Quando `Inverter` é jogada, a direção da fila se inverte (`Fila.inverter`, chamado dentro de `JogoUno.jogar_carta`).

| Antes (ordem da fila) | Depois de Inverter |
|---|---|
| A → B → C → D | D → C → B → A |

A inversão ocorre **antes** de o jogador da vez voltar para o fim da fila, garantindo que a ordem dos demais já saia correta.

## RN08 — Efeito das Cartas +2 e +4

Cartas `+2` e `+4` forçam o próximo jogador a comprar cartas e perder a vez (`JogoUno._aplicar_efeito_no_proximo`).

| Carta jogada | Cartas que o próximo jogador compra | Próximo jogador joga? |
|---|---|---|
| `+2` | 2 | Não — é pulado |
| `+4` (Curinga) | 4 | Não — é pulado |

## RN09 — Compra Automática sem Jogada Válida

Se o jogador não tiver nenhuma carta jogável, ele compra 1 carta e passa a vez (`JogoUno.comprar_e_passar`).

| Situação | Ação do motor |
|---|---|
| `cartas_validas(jogador)` retorna lista vazia | Interface deve chamar `comprar_e_passar()` |
| `comprar_e_passar()` chamado | Retira o jogador da fila, compra 1 carta, devolve ao fim da fila |

## RN10 — Reciclagem do Monte de Compra

Se o `monte_compra` ficar vazio durante uma compra, o `monte_descarte` é reaproveitado (`JogoUno._reciclar_descarte`).

| Condição | Ação |
|---|---|
| `monte_descarte.tamanho() <= 1` | Não recicla (não há cartas suficientes) |
| `monte_descarte.tamanho() > 1` | Guarda a carta do topo, move o restante para `monte_compra`, embaralha, devolve o topo ao descarte |

## RN11 — Aviso de UNO

Quando um jogador fica com exatamente 1 carta após jogar, o motor registra um aviso no `log` (`JogoUno.jogar_carta`).

| Cartas restantes após a jogada | Mensagem no log |
|---|---|
| 1 | `"*** {nome} gritou UNO! ***"` |
| Qualquer outro valor | Nenhuma mensagem de UNO |

## RN12 — Condição de Vitória

O jogador que fica sem cartas na mão vence a partida imediatamente (`Jogador.sem_cartas`, checado em `JogoUno.jogar_carta`).

| Situação | Resultado |
|---|---|
| Jogador joga sua última carta | `jogo.vencedor` recebe esse jogador; nenhum efeito especial é aplicado depois |
| `jogo.acabou()` passa a retornar `True` | Novas chamadas a `jogar_carta`/`comprar_e_passar` levantam `ValueError` |

## RN13 — Montagem do Ranking (Árvore Binária de Busca)

O ranking é montado inserindo cada jogador em uma [`ArvoreBinariaBusca`](../componentes/arvore-binaria-busca.md) com chave = quantidade de cartas (`JogoUno.ranking`).

| Passo | Descrição |
|---|---|
| 1 | Cria uma árvore nova (vazia) |
| 2 | Insere cada jogador da fila com `inserir(quantidade_cartas, nome)` |
| 3 | Se já houver vencedor, insere-o também com chave `0` |
| 4 | Percorre a árvore `em_ordem()` (esquerda → raiz → direita) |
| 5 | Resultado: lista ordenada do menor para o maior número de cartas, sem usar `sort()` |

**Exemplo:** Matheus com 3 cartas, Bot Ana com 1, Bot Beto com 7 → ranking: Bot Ana (1), Matheus (3), Bot Beto (7).

## RN14 — Estratégia de Jogada do Bot

A "inteligência" do bot segue uma ordem fixa de preferência (`bot.escolher_jogada`).

| Situação | Decisão do bot |
|---|---|
| Não há carta válida | Retorna `(None, None)` → quem chamou deve comprar |
| Há cartas válidas comuns (não-Curinga) | Sorteia uma entre elas |
| Só há Curinga válido | Sorteia entre os curingas válidos |
| Jogada escolhida é Curinga | Escolhe a cor mais frequente na própria mão (`_cor_mais_frequente`) |
| Mão sem nenhuma cor normal | Sorteia uma cor aleatória entre `CORES` |

## Links Relacionados

- [`JogoUno`](../componentes/jogo-uno.md) — implementação de quase todas as regras acima.
- [`Carta`](../componentes/carta.md) — RN04, RN05.
- [`Fila`](../componentes/fila.md) — RN06, RN07, RN08.
- [`Pilha`](../componentes/pilha.md) — RN01, RN03, RN10.
- [`ArvoreBinariaBusca`](../componentes/arvore-binaria-busca.md) — RN13.
- [`bot`](../componentes/bot.md) — RN14.

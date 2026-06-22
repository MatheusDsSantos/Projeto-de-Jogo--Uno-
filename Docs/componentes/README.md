# Mapa dos Componentes

Este projeto é organizado em três grupos: **estruturas de dados** (a base acadêmica do projeto), **modelo/domínio** (as regras do UNO) e **interfaces** (as formas de jogar).

## Estruturas de Dados

| Componente | Arquivo | Responsabilidade principal |
|---|---|---|
| [`Pilha`](pilha.md) | `estruturas/pilha.py` | Monte de compra e monte de descarte (LIFO) |
| [`Fila`](fila.md) | `estruturas/fila.py` | Ordem dos turnos dos jogadores (FIFO) |
| [`ListaEncadeada`](lista-encadeada.md) | `estruturas/lista_encadeada.py` | Mão de cartas de cada jogador |
| [`ArvoreBinariaBusca`](arvore-binaria-busca.md) | `estruturas/arvore.py` | Ranking dos jogadores por quantidade de cartas |

## Modelo / Domínio

| Componente | Arquivo | Responsabilidade principal |
|---|---|---|
| [`Carta`](carta.md) | `modelo/carta.py` | Representar uma carta e a regra de combinação |
| [`Jogador`](jogador.md) | `modelo/jogador.py` | Um participante e sua mão de cartas |
| [`JogoUno`](jogo-uno.md) | `modelo/jogo.py` | Motor do jogo: todas as regras, sem entrada/saída |
| [`bot`](bot.md) | `modelo/bot.py` | Estratégia de jogada dos jogadores-computador |

## Interfaces

| Componente | Arquivo | Responsabilidade principal |
|---|---|---|
| [Terminal (`uno.py`)](terminal-uno.md) | `uno.py` | Jogo via teclado, 2 a 4 jogadores humanos |
| [Servidor Web (`servidor.py`)](servidor-web.md) | `servidor.py` | API JSON + arquivos estáticos do frontend |
| [Interface Web (`frontend/`)](interface-web.md) | `frontend/script.js`, `index.html`, `style.css` | Tabuleiro no navegador, consumindo a API |

## Regra de Ouro

> O motor (`JogoUno`) nunca fala diretamente com o usuário, e nenhuma interface implementa regra de jogo por conta própria.

Toda decisão de "isso pode ou não pode" mora em [`JogoUno`](jogo-uno.md) ou nos objetos de domínio (`Carta`, `Jogador`). As interfaces apenas coletam a entrada do usuário, chamam o motor e exibem o resultado.

## Como os Dados Caminham

```
entrada do usuário (teclado ou clique)
        │
        ▼
interface (uno.py  OU  servidor.py + frontend/)
        │  chama métodos públicos
        ▼
JogoUno (motor / regras)
        │  usa
        ▼
Pilha · Fila · ListaEncadeada (dentro de Jogador) · ArvoreBinariaBusca (em ranking())
        │  manipulam
        ▼
Carta
```

- No terminal, a cadeia é direta: `uno.py → JogoUno → estruturas`.
- Na web, existe um salto HTTP/JSON: `frontend/script.js → servidor.py → JogoUno → estruturas`.

Veja o detalhamento gráfico em [Diagrama de Arquitetura](../arquitetura/diagrama.md).

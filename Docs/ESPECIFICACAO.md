# Especificação — Jogo UNO (Estruturas de Dados)

## Resumo

Este projeto é um jogo de UNO em Python que existe para demonstrar, de forma prática, quatro estruturas de dados clássicas: **Pilha**, **Fila**, **Lista Encadeada** e **Árvore Binária de Busca**. O mesmo motor de regras (`JogoUno`) é consumido por duas interfaces independentes: terminal (`uno.py`) e navegador (`servidor.py` + `frontend/`).

| Estrutura | Onde é usada |
|---|---|
| Pilha (LIFO) | Monte de compra e monte de descarte |
| Fila (FIFO) | Ordem dos turnos dos jogadores |
| Lista Encadeada | Mão de cartas de cada jogador |
| Árvore Binária de Busca | Ranking dos jogadores, sem usar `sort()` |

## Mapa da Documentação

### Projeto

- [Escopo](projeto/escopo.md) — o que o sistema entrega, o que está fora do escopo, decisões de projeto.
- [Roteiro de Implementação](projeto/roteiro-de-implementacao.md) — ordem sugerida para construir o projeto.

### Regras de Negócio

- [Regras de Negócio](regras/regras-de-negocio.md) — RN01 a RN14, com tabelas de condição/resultado e exemplos.

### Componentes

- [Mapa de Componentes](componentes/README.md) — visão geral por grupo (estruturas / domínio / interfaces).

**Estruturas de dados:**

- [`Pilha`](componentes/pilha.md)
- [`Fila`](componentes/fila.md)
- [`ListaEncadeada`](componentes/lista-encadeada.md)
- [`ArvoreBinariaBusca`](componentes/arvore-binaria-busca.md)

**Modelo / domínio:**

- [`Carta`](componentes/carta.md)
- [`Jogador`](componentes/jogador.md)
- [`JogoUno`](componentes/jogo-uno.md)
- [`bot`](componentes/bot.md)

**Interfaces:**

- [Terminal (`uno.py`)](componentes/terminal-uno.md)
- [Servidor Web (`servidor.py`)](componentes/servidor-web.md)
- [Interface Web (`frontend/`)](componentes/interface-web.md)

### Arquitetura

- [Diagrama de Arquitetura](arquitetura/diagrama.md) — diagrama de classes e fluxo de requisição.
- [Estrutura de Pastas](arquitetura/estrutura-de-pastas.md) — árvore do projeto e arquitetura em camadas.

### Padrões

- [Padrões do Projeto](padroes/padroes-do-projeto.md) — convenções de nomenclatura, organização e estilo.

## Leitura Recomendada

| Se você quer... | Comece por... |
|---|---|
| Entender o projeto em 5 minutos | Este arquivo + [Mapa de Componentes](componentes/README.md) |
| Ver como uma regra específica do UNO funciona | [Regras de Negócio](regras/regras-de-negocio.md) |
| Entender uma estrutura de dados específica | A página dela em `componentes/` (ex.: [`Pilha`](componentes/pilha.md)) |
| Ver as classes e suas relações de uma vez | [Diagrama de Arquitetura](arquitetura/diagrama.md) |
| Recriar o projeto do zero, passo a passo | [Roteiro de Implementação](projeto/roteiro-de-implementacao.md) |
| Saber o que o projeto **não** faz | [Escopo](projeto/escopo.md#fora-do-escopo) |

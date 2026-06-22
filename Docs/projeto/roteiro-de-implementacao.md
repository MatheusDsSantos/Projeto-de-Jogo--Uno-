# Roteiro de Implementação

Ordem sugerida para construir (ou recriar, em outra linguagem) este projeto do zero, da camada mais baixa para a mais alta — coerente com a [arquitetura em camadas](../arquitetura/estrutura-de-pastas.md#arquitetura-em-camadas).

## 1. Estruturas de Dados Puras

Implementar cada estrutura isoladamente, sem nenhuma referência ao UNO:

1. [`Pilha`](../componentes/pilha.md) — `empurrar`, `retirar`, `ver_topo`, `esta_vazia`, `tamanho`, `embaralhar`.
2. [`Fila`](../componentes/fila.md) — `entrar`, `proximo`, `ver_primeiro`, `inverter`, `listar`.
3. [`ListaEncadeada`](../componentes/lista-encadeada.md) (com `No`) — `adicionar`, `remover_por_indice`, `listar`.
4. [`ArvoreBinariaBusca`](../componentes/arvore-binaria-busca.md) (com `NoArvore`) — `inserir`, `em_ordem`, `buscar`, `altura`.

> Critério de pronto: cada estrutura testável isoladamente (ex.: empilhar e desempilhar números, sem precisar de `Carta`).

## 2. Modelo de Domínio

5. [`Carta`](../componentes/carta.md) — atributos `cor`/`valor` e a regra `pode_jogar_sobre`.
6. [`Jogador`](../componentes/jogador.md) — usa a `ListaEncadeada` da etapa 1 para a mão.

## 3. Motor do Jogo

7. [`JogoUno`](../componentes/jogo-uno.md) — nesta ordem interna:
   - Preparação: `_criar_baralho`, `_distribuir_cartas`, `_virar_primeira_carta` (ver [RN01–RN03](../regras/regras-de-negocio.md)).
   - Consultas: `jogador_da_vez`, `carta_do_topo`, `cartas_validas`.
   - Ação principal: `jogar_carta` (validação → aplicação → efeitos especiais → checagem de vitória).
   - Ação secundária: `comprar_e_passar`, `_comprar_carta`, `_reciclar_descarte`.
   - Ranking: `ranking()`, usando a `ArvoreBinariaBusca` da etapa 1.

> Critério de pronto: uma partida completa simulável por código (sem interface), do início até um vencedor.

## 4. Estratégia do Bot

8. [`bot.escolher_jogada`](../componentes/bot.md) — depende apenas de `JogoUno.cartas_validas` e `Jogador.cartas`, já prontos na etapa 3.

## 5. Interface de Terminal

9. [`uno.py`](../componentes/terminal-uno.md) — laço de configuração → laço de turnos → exibição de log e ranking.

> Critério de pronto: `python uno.py` permite jogar uma partida completa por teclado.

## 6. Servidor Web e API

10. [`servidor.py`](../componentes/servidor-web.md) — nesta ordem:
    - `estado_do_jogo()` (serialização do estado atual).
    - Rota `/api/novo-jogo` (`acao_novo_jogo`).
    - Rota `/api/jogar` (`acao_jogar`).
    - Rota `/api/comprar` (`acao_comprar`).
    - Rota `/api/bot-jogar` (`acao_bot_jogar`).
    - Classe `ServidorUno` ligando as rotas HTTP às funções acima.

## 7. Interface Web

11. [`frontend/index.html`](../componentes/interface-web.md) — esqueleto das telas (inicial, mesa de jogo, modais).
12. `frontend/style.css` — estilo visual.
13. `frontend/script.js` — `chamarApi`, `renderizar`, ações do jogador (`jogarCarta`, `comprarCarta`, `escolherCor`), laço de bots (`rodarBots`).

> Critério de pronto: `python servidor.py` + navegador em `http://localhost:8000` permite jogar contra bots.

## 8. Camada Educacional (Botões Informativos)

14. Objeto `INFO_ESTRUTURAS` em `script.js` com a explicação de cada estrutura de dados.
15. Botões `.btn-info` posicionados ao lado de cada uso visível (monte de compra/descarte, ordem dos turnos, mão do jogador, ranking).
16. Modal `#modal-info` reaproveitado para todas as explicações, trocando conteúdo e cor de cabeçalho conforme a estrutura clicada.

## Links Relacionados

- [Escopo do Projeto](escopo.md)
- [Regras de Negócio](../regras/regras-de-negocio.md)
- [Mapa de Componentes](../componentes/README.md)
- [Diagrama de Arquitetura](../arquitetura/diagrama.md)

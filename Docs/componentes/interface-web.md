# Interface `frontend/` (Interface Web)

## Objetivo

Renderizar o tabuleiro do UNO no navegador e conversar com o [servidor web](servidor-web.md) via `fetch`, sem nenhum framework — HTML, CSS e JavaScript puros.

## Responsabilidades

- Montar a tela inicial (nome do jogador, quantidade de bots) e a mesa de jogo.
- Chamar a API JSON do servidor e renderizar o estado retornado (`renderizar`).
- Tratar os cliques do jogador: jogar carta, escolher cor de curinga, comprar carta.
- Encadear automaticamente as jogadas dos bots (`rodarBots`) até a vez voltar ao humano.
- Exibir, sob demanda, explicações sobre qual estrutura de dados está em uso em cada parte da tela (botões `?`).

## Papel no Fluxo

`script.js` é o único arquivo com lógica do frontend; `index.html` define a estrutura da página e `style.css` o visual.

| Ação do usuário | Função acionada | Rota chamada |
|---|---|---|
| Clica em "Começar jogo" | `iniciarJogo()` | `POST /api/novo-jogo` |
| Clica em uma carta jogável | `jogarCarta(indice, carta)` | `POST /api/jogar` |
| Escolhe a cor de um curinga | `escolherCor(cor)` | `POST /api/jogar` (com `cor`) |
| Clica no monte de compra | `comprarCarta()` | `POST /api/comprar` |
| Vez de um bot (automático) | `rodarBots(estado)` | `POST /api/bot-jogar` (em laço) |
| Clica em um botão `?` | listener de `.btn-info` | nenhuma (usa dados locais de `INFO_ESTRUTURAS`) |

## Atributos / Estado

```javascript
let botsEscolhidos = 2;
let meuNome = "";
let indiceCuringa = null;  // carta curinga aguardando escolha de cor
let rodandoBots = false;   // evita dois laços de bot simultâneos

const CLASSES_COR = { Vermelho, Azul, Verde, Amarelo, Curinga };
const CORES_HEX = { Vermelho, Azul, Verde, Amarelo };
const SIMBOLOS = { Pular: "⦸", Inverter: "⇄", Curinga: "W" };

const INFO_ESTRUTURAS = {
  "pilha-compra": { icone, titulo, tag, tagClasse, headerClasse, texto, metodos },
  "pilha-descarte": { /* idem */ },
  "fila": { /* idem */ },
  "lista": { /* idem */ },
  "abb": { /* idem */ },
};
```

## Métodos / Funções

```javascript
async function chamarApi(rota, corpo)
function simboloDe(valor)
function criarCartaHTML(carta)
function renderizar(estado)
async function jogarCarta(indice, carta)
async function escolherCor(cor)
async function comprarCarta()
async function executar(acao)
async function rodarBots(estado)
async function iniciarJogo()
```

A seção final do arquivo registra os listeners de clique (botões de bots, iniciar, comprar, escolher cor, jogar novamente, reiniciar) e a lógica dos botões informativos (`.btn-info` → preenche e abre `#modal-info`).

## Validações

- `chamarApi` lança `Error(dados.erro || "Erro no servidor")` quando a resposta HTTP não é `ok`; `executar` captura esse erro e mostra a mensagem em `#aviso-vez`.
- `renderizar` só permite clicar em cartas que estejam em `estado.jogaveis` **e** quando `estado.vez_humano` for verdadeiro.

## Não Deve Fazer

- Não decide se uma jogada é válida — apenas reflete a lista `jogaveis` que vem do [servidor](servidor-web.md)/[`JogoUno`](jogo-uno.md).
- Não guarda o estado da partida entre recarregamentos de página — tudo vem da API a cada ação.

## Exemplo de Uso

```javascript
// Disparado ao clicar em uma carta jogável
async function jogarCarta(indice, carta) {
  if (carta.cor === "Curinga") {
    indiceCuringa = indice;
    modalCor.classList.remove("escondida");
    return;
  }
  await executar(() => chamarApi("/api/jogar", { indice }));
}
```

## Links Relacionados

- [Servidor Web](servidor-web.md) — back-end consumido por todas as chamadas `chamarApi`.
- [`Pilha`](pilha.md), [`Fila`](fila.md), [`ListaEncadeada`](lista-encadeada.md), [`ArvoreBinariaBusca`](arvore-binaria-busca.md) — estruturas explicadas pelos botões informativos.

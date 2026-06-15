# Jogo UNO — Estruturas de Dados

Jogo de UNO em Python demonstrando o uso de **quatro estruturas de dados**:

| Estrutura | Arquivo | Onde é usada |
|---|---|---|
| **Pilha** (LIFO) | `estruturas/pilha.py` | Monte de compra e monte de descarte |
| **Fila** (FIFO) | `estruturas/fila.py` | Ordem dos turnos dos jogadores |
| **Lista Encadeada** | `estruturas/lista_encadeada.py` | Mão de cartas de cada jogador |
| **Árvore Binária de Busca** | `estruturas/arvore.py` | Ranking dos jogadores (percurso em ordem) |

## Como rodar

Não precisa instalar nada — só Python 3 (biblioteca padrão).

**Versão web (navegador):**

```
python servidor.py
```

Depois abra **http://localhost:8000** no navegador. Você joga contra 1 a 3 bots.

**Versão terminal (2 a 4 jogadores no mesmo teclado):**

```
python uno.py
```

## Estrutura do projeto

```
projeto_Uno/
├── uno.py                  # Interface de terminal
├── servidor.py             # Servidor web (http.server) + API JSON
├── estruturas/             # Estruturas de dados
│   ├── pilha.py            # Pilha (montes de cartas)
│   ├── fila.py             # Fila (turnos)
│   ├── lista_encadeada.py  # Lista encadeada (mão do jogador)
│   └── arvore.py           # Árvore Binária de Busca (ranking)
├── modelo/                 # Regras do jogo
│   ├── carta.py            # Carta e regra de combinação
│   ├── jogador.py          # Jogador e sua mão
│   ├── jogo.py             # Motor do jogo (sem entrada/saída)
│   └── bot.py              # Estratégia dos jogadores-computador
└── frontend/               # Interface web (HTML/CSS/JS puro)
    ├── index.html
    ├── style.css
    └── script.js
```

## Arquitetura

O **motor do jogo** (`modelo/jogo.py`) contém todas as regras mas não faz
`input()` nem `print()`. Quem conversa com o usuário são as interfaces:

- `uno.py` lê o teclado e imprime no terminal;
- `servidor.py` expõe uma **API JSON** que o frontend consome via `fetch`.

```
navegador (frontend/) ──HTTP/JSON──► servidor.py ──► modelo/jogo.py ──► estruturas/
terminal  (uno.py)    ────────────────────────────►
```

### Onde entra a Árvore Binária de Busca

A cada jogada, o método `JogoUno.ranking()` insere cada jogador na ABB
usando a **quantidade de cartas na mão como chave**. O **percurso em ordem**
(esquerda → raiz → direita) devolve os jogadores automaticamente ordenados
do que tem menos cartas (ganhando) para o que tem mais (perdendo) — sem
usar `sort()`. O resultado aparece no painel "Ranking" da interface web e
no fim da partida no terminal.

## API do servidor

| Método | Rota | Corpo | Ação |
|---|---|---|---|
| POST | `/api/novo-jogo` | `{"nome": "Matheus", "bots": 2}` | Cria nova partida |
| GET | `/api/estado` | — | Estado atual do jogo |
| POST | `/api/jogar` | `{"indice": 3, "cor": "Azul"}` | Humano joga carta (cor só p/ curinga) |
| POST | `/api/comprar` | — | Humano compra 1 carta e passa |
| POST | `/api/bot-jogar` | — | Executa uma jogada do bot da vez |

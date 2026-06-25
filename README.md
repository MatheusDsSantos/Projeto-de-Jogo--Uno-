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

## Ciclo completo do jogo

### 1. Onde o jogo inicia
- Terminal: execute `python uno.py` na pasta do projeto.
- Web: execute `python servidor.py` na pasta do projeto e depois abra
  `http://localhost:8000`.

### 2. Onde a classe do motor é criada
- A classe `JogoUno` está em `modelo/jogo.py`.
- Ela é responsável por criar e embaralhar o baralho, distribuir cartas,
  virar a primeira carta, validar jogadas, aplicar efeitos, comprar cartas
  e controlar quando o jogo termina.

### 3. Como a classe é chamada
#### Em `uno.py`
- `main()` cria os jogadores com `Jogador(nome)` e em seguida cria o jogo com
  `JogoUno(jogadores)`.
- Ao instanciar `JogoUno`, o construtor chama internamente:
  - `_criar_baralho()`
  - `_distribuir_cartas()`
  - `_virar_primeira_carta()`
- Depois, o jogo entra no loop principal, que em cada rodada chama:
  - `turno(jogo)`
  - `mostrar_novidades(jogo, mensagens_mostradas)`
- Dentro de `turno(jogo)`:
  - se o jogador não tem carta válida, chama `jogo.comprar_e_passar()`;
  - se escolhe comprar, chama `jogo.comprar_e_passar()`;
  - se escolhe jogar, chama `jogo.jogar_carta(indice, cor)`.

#### Em `servidor.py`
- O servidor mantém um objeto `jogo` em memória.
- As rotas da API chamam métodos de `JogoUno`:
  - `/api/novo-jogo` cria `JogoUno(jogadores)` em `acao_novo_jogo(dados)`;
  - `/api/estado` lê o estado atual em `estado_do_jogo()`;
  - `/api/jogar` chama `acao_jogar(dados)` que executa `jogo.jogar_carta(indice, cor)`;
  - `/api/comprar` chama `acao_comprar()` que executa `jogo.comprar_e_passar()`;
  - `/api/bot-jogar` chama `acao_bot_jogar()`, que usa `modelo/bot.py` para escolher
    a jogada do bot.

### 4. Onde estão os arquivos principais
- `uno.py`: interface de terminal.
- `servidor.py`: servidor web e API.
- `modelo/jogo.py`: motor do jogo.
- `modelo/jogador.py`: classe `Jogador`.
- `modelo/carta.py`: classe `Carta`.
- `modelo/bot.py`: lógica dos bots.
- `estruturas/`: implementação de fila, pilha, lista encadeada e árvore.
- `frontend/`: interface web em HTML, CSS e JavaScript.

### 5. Resumo do fluxo
- `uno.py` ou `servidor.py` são as portas de entrada do programa.
- Eles criam `JogoUno` e chamam seus métodos públicos.
- `JogoUno` usa as estruturas para controlar turnos, mãos, baralho, descarte
  e ranking.
- A interface não implementa regras; ela apenas pergunta, mostra e envia
  ações para o motor do jogo.

## API do servidor

| Método | Rota | Corpo | Ação |
|---|---|---|---|
| POST | `/api/novo-jogo` | `{"nome": "Matheus", "bots": 2}` | Cria nova partida |
| GET | `/api/estado` | — | Estado atual do jogo |
| POST | `/api/jogar` | `{"indice": 3, "cor": "Azul"}` | Humano joga carta (cor só p/ curinga) |
| POST | `/api/comprar` | — | Humano compra 1 carta e passa |
| POST | `/api/bot-jogar` | — | Executa uma jogada do bot da vez |

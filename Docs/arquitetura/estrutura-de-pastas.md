# Estrutura de Pastas

## Árvore do Projeto

```
projeto_Uno/
├── uno.py                  # Interface de terminal
├── servidor.py              # Servidor web (http.server) + API JSON
├── estruturas/               # Estruturas de dados
│   ├── __init__.py
│   ├── pilha.py              # Pilha (montes de cartas)
│   ├── fila.py                # Fila (turnos)
│   ├── lista_encadeada.py    # Lista encadeada (mão do jogador)
│   └── arvore.py              # Árvore Binária de Busca (ranking)
├── modelo/                   # Regras do jogo
│   ├── __init__.py
│   ├── carta.py               # Carta e regra de combinação
│   ├── jogador.py             # Jogador e sua mão
│   ├── jogo.py                 # Motor do jogo (sem entrada/saída)
│   └── bot.py                  # Estratégia dos jogadores-computador
├── frontend/                 # Interface web (HTML/CSS/JS puro)
│   ├── index.html
│   ├── style.css
│   └── script.js
└── Docs/                      # Esta documentação
```

## Arquitetura em Camadas

O projeto não usa um framework MVC, mas segue uma separação em camadas clara, de baixo para cima:

| Camada | Pasta | Depende de | Não depende de |
|---|---|---|---|
| 1. Estruturas de dados | `estruturas/` | nada do projeto (só `random`, `collections`) | `modelo/`, interfaces |
| 2. Modelo / domínio | `modelo/` | `estruturas/` | interfaces (`uno.py`, `servidor.py`, `frontend/`) |
| 3. Interfaces | `uno.py`, `servidor.py`, `frontend/` | `modelo/` (as duas primeiras) | — |

Essa ordem é uma via de mão única: `estruturas/` nunca importa de `modelo/`, e `modelo/` nunca importa de `uno.py`/`servidor.py`. Isso é o que permite o mesmo motor (`modelo/jogo.py`) funcionar tanto no terminal quanto na web — ver [Mapa de Componentes](../componentes/README.md#regra-de-ouro).

A camada de interfaces tem dois ramos independentes que nunca se comunicam entre si:

- **Terminal:** `uno.py` → `modelo/`.
- **Web:** `frontend/` → (HTTP/JSON) → `servidor.py` → `modelo/`.

## Responsabilidade de Cada Pasta

| Pasta/Arquivo | Responsabilidade |
|---|---|
| `estruturas/` | Implementações próprias de Pilha, Fila, Lista Encadeada e Árvore Binária de Busca — o conteúdo acadêmico central do projeto. |
| `modelo/` | Regras do UNO: o que é uma carta válida, como os turnos avançam, quando alguém vence. |
| `uno.py` | Único ponto de entrada para jogar pelo terminal. |
| `servidor.py` | Único ponto de entrada para jogar pelo navegador; expõe a API JSON e os arquivos estáticos. |
| `frontend/` | HTML, CSS e JavaScript da interface visual, sem nenhuma regra de jogo embutida. |
| `Docs/` | Documentação do projeto (este diretório). |

## Links Relacionados

- [Diagrama de Arquitetura](diagrama.md)
- [Mapa de Componentes](../componentes/README.md)
- [Padrões do Projeto](../padroes/padroes-do-projeto.md)

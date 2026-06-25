# Padrões do Projeto

## Linguagem

## Nomenclatura

| Elemento | Convenção | Exemplo |
|---|---|---|
| Classe | `PascalCase` | `JogoUno`, `ArvoreBinariaBusca`, `ListaEncadeada` |
| Função / método | `snake_case` | `pode_jogar_sobre`, `comprar_e_passar` |
| Variável / atributo | `snake_case` | `cor_atual`, `monte_descarte` |
| Método/atributo "interno" | prefixo `_` | `_criar_baralho`, `_cartas`, `_jogadores` |
| Constante de classe | `MAIUSCULO` | `JogoUno.CORES`, `JogoUno.VALORES_ESPECIAIS` |
| Rota de API | `/api/` + cinemática em português | `/api/novo-jogo`, `/api/bot-jogar` |
| Variável JS | `camelCase` em português | `botsEscolhidos`, `indiceCuringa`, `rodandoBots` |
| Classe/ID CSS | `kebab-case` em português | `.botao-principal`, `#area-oponentes` |

O prefixo `_` indica "não chamar de fora da classe" por convenção — Python não impõe isso, mas o projeto é consistente: todo método auxiliar interno de `Pilha`, `Fila` e `JogoUno` recebe esse prefixo.

## Organização de Arquivos

- Um conceito por arquivo: cada estrutura de dados (`pilha.py`, `fila.py`, `lista_encadeada.py`, `arvore.py`) vive isolada em `estruturas/`.
- O domínio do jogo fica em `modelo/`, separado das estruturas de dados genéricas.
- Cada pacote (`estruturas/`, `modelo/`) tem um `__init__.py` que reexporta as classes principais, permitindo `from estruturas import Pilha` em vez de `from estruturas.pilha import Pilha`.
- As duas interfaces (`uno.py` terminal e `servidor.py` + `frontend/` web) ficam fora dos pacotes, na raiz do projeto.

## Comentários e Docstrings

- Todo arquivo começa com uma docstring de módulo em bloco (`"""..."""`) explicando o papel daquele arquivo em 1-3 linhas, sempre em CAIXA ALTA no título: `"""PILHA (Stack) - usada para..."""`.
- Toda classe tem uma docstring de uma linha repetindo seu propósito.
- Comentários de linha (`#`) são usados para explicar **por quê**, não **o quê** — por exemplo, em `jogo.py`, o comentário sobre o efeito Inverter explica a ordem de execução escolhida, não repete o nome do método.

## Estilo de Código Python

- Sem type hints e sem dependências externas — todo o backend usa apenas a biblioteca padrão (`random`, `collections.deque`, `http.server`, `json`, `threading`).
- Funções/métodos que **consultam** o estado (não alteram nada) ficam agrupadas e comentadas como `CONSULTAS`; funções que **alteram** o estado ficam agrupadas como `ACOES` (ver `modelo/jogo.py`).
- Erros de regra de negócio são sempre `ValueError`, nunca exceções customizadas.
- Métodos que podem "não encontrar nada" (`retirar`, `proximo`, `ver_topo`) retornam `None` em vez de levantar exceção; quem decide se isso é um erro é a camada de cima.

## Estilo de Código Frontend

- `index.html`, `style.css` e `script.js` são arquivos únicos, sem bundler nem build step.
- Comunicação com o backend é centralizada em uma única função (`chamarApi`), nunca chamando `fetch` diretamente em outros lugares.
- Conteúdo educacional (explicação das estruturas de dados) fica isolado em um objeto de dados (`INFO_ESTRUTURAS`) separado da lógica de renderização do jogo.

## Links Relacionados

- [Estrutura de Pastas](../arquitetura/estrutura-de-pastas.md)
- [Mapa de Componentes](../componentes/README.md)

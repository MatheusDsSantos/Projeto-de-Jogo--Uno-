# Diagrama de Arquitetura

## Resumo dos Componentes

| Grupo | Componentes |
|---|---|
| Estruturas de dados | `Pilha`, `Fila`, `No` + `ListaEncadeada`, `NoArvore` + `ArvoreBinariaBusca` |
| Modelo / domínio | `Carta`, `Jogador`, `JogoUno`, módulo `bot` |
| Interfaces | `uno.py` (terminal), `ServidorUno` + funções de ação (web), `frontend/script.js` |

## Relações Principais

| Origem | Relação | Destino | Observação |
|---|---|---|---|
| `JogoUno` | composição | `Pilha` | dois atributos: `monte_compra` e `monte_descarte` |
| `JogoUno` | composição | `Fila` | atributo `fila_jogadores` |
| `JogoUno` | uso | `ArvoreBinariaBusca` | criada e descartada dentro de `ranking()`, não é atributo persistente |
| `JogoUno` | uso | `Carta` | cria as 108 cartas do baralho e cartas de referência para validação |
| `Fila` | agregação | `Jogador` | jogadores existem fora da fila; a fila só os ordena |
| `Jogador` | composição | `ListaEncadeada` | atributo `mao`, exclusivo de cada jogador |
| `ListaEncadeada` | composição | `No` | cadeia de nós |
| `No` | uso | `Carta` | cada nó guarda uma carta |
| `ArvoreBinariaBusca` | composição | `NoArvore` | árvore de nós |
| `NoArvore` | composição | `NoArvore` | `esquerda` e `direita` |
| `bot` | uso | `JogoUno`, `Jogador`, `Carta` | módulo de funções, sem estado próprio |
| `ServidorUno` | uso | `JogoUno`, `Jogador` | cria e consulta a partida em memória |
| `frontend/script.js` | uso (via HTTP/JSON) | `servidor.py` | não há relação de código direta, apenas chamadas `fetch` |

## Diagrama de Classes

```mermaid
classDiagram
    class Pilha {
        -_cartas: list
        +empurrar(carta)
        +retirar() Carta
        +ver_topo() Carta
        +esta_vazia() bool
        +tamanho() int
        +embaralhar()
    }

    class Fila {
        -_jogadores: deque
        +entrar(jogador)
        +proximo() Jogador
        +ver_primeiro() Jogador
        +inverter()
        +listar() list
        +esta_vazia() bool
        +quantidade() int
    }

    class No {
        +carta: Carta
        +proximo: No
    }

    class ListaEncadeada {
        +inicio: No
        +tamanho: int
        +adicionar(carta)
        +remover_por_indice(indice) Carta
        +listar() list
        +esta_vazia() bool
    }

    class NoArvore {
        +chave: int
        +valor: str
        +esquerda: NoArvore
        +direita: NoArvore
    }

    class ArvoreBinariaBusca {
        +raiz: NoArvore
        +inserir(chave, valor)
        +em_ordem() list
        +buscar(chave) str
        +altura() int
    }

    class Carta {
        +cor: str
        +valor: str
        +pode_jogar_sobre(carta_do_topo) bool
        +para_dicionario() dict
    }

    class Jogador {
        +nome: str
        +eh_bot: bool
        +mao: ListaEncadeada
        +receber_carta(carta)
        +jogar_carta(indice) Carta
        +cartas() list
        +tem_carta_valida(carta_do_topo, cor_atual) bool
        +quantidade_cartas() int
        +sem_cartas() bool
    }

    class JogoUno {
        +CORES: list
        +VALORES_NORMAIS: list
        +VALORES_ESPECIAIS: list
        +monte_compra: Pilha
        +monte_descarte: Pilha
        +fila_jogadores: Fila
        +cor_atual: str
        +vencedor: Jogador
        +log: list
        +jogador_da_vez() Jogador
        +carta_do_topo() Carta
        +acabou() bool
        +cartas_validas(jogador) list
        +ranking() list
        +registrar(mensagem)
        +jogar_carta(indice, cor_escolhida) Carta
        +comprar_e_passar()
    }

    class bot {
        <<module>>
        +escolher_jogada(jogo, jogador) tuple
    }

    class ServidorUno {
        +do_GET()
        +do_POST()
    }

    ListaEncadeada "1" *-- "0..many" No : contém
    No "1" --> "0..1" No : proximo
    No --> Carta : guarda
    ArvoreBinariaBusca "1" *-- "0..many" NoArvore : contém
    NoArvore --> NoArvore : esquerda / direita
    Jogador "1" *-- "1" ListaEncadeada : mao
    JogoUno "1" *-- "2" Pilha : monte_compra / monte_descarte
    JogoUno "1" *-- "1" Fila : fila_jogadores
    Fila "1" o-- "0..many" Jogador : ordena
    JogoUno ..> ArvoreBinariaBusca : usa em ranking()
    JogoUno ..> Carta : cria / valida
    bot ..> JogoUno : usa
    bot ..> Jogador : usa
    bot ..> Carta : usa
    ServidorUno ..> JogoUno : controla
```

## Fluxo de Requisição (Navegador → Motor)

```mermaid
flowchart LR
    Nav["Navegador<br/>(frontend/)"] -->|fetch HTTP/JSON| Srv["servidor.py<br/>(ServidorUno)"]
    Term["Terminal<br/>(uno.py)"] --> Motor
    Srv --> Motor["modelo/jogo.py<br/>(JogoUno)"]
    Motor --> Estr["estruturas/<br/>Pilha · Fila · ListaEncadeada · ArvoreBinariaBusca"]
    Motor --> Dom["modelo/<br/>Carta · Jogador"]
    Srv -.bot da vez.-> Bot["modelo/bot.py"]
    Bot --> Motor
```

## Links Relacionados

- [Mapa de Componentes](../componentes/README.md)
- [Estrutura de Pastas](estrutura-de-pastas.md)
- [Regras de Negócio](../regras/regras-de-negocio.md)

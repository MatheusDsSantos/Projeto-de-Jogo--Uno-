# Componente de Domínio `JogoUno`

## Objetivo

Ser o motor do jogo: concentra todas as regras do UNO sem fazer `input()` nem `print()`, para poder ser reaproveitado tanto pelo terminal quanto pelo servidor web.

## Responsabilidades

- Montar e embaralhar o baralho de 108 cartas.
- Distribuir 7 cartas para cada jogador.
- Controlar de quem é a vez (via [`Fila`](fila.md)).
- Validar e aplicar jogadas (`jogar_carta`).
- Aplicar efeitos das cartas especiais (Pular, Inverter, +2, +4).
- Controlar a compra de cartas, incluindo a reciclagem do monte de descarte.
- Detectar a vitória e manter o histórico (`log`) da partida.
- Montar o ranking dos jogadores usando a [`ArvoreBinariaBusca`](arvore-binaria-busca.md).

## Papel no Fluxo

`JogoUno` é instanciado uma vez por partida, recebendo a lista de [`Jogador`](jogador.md) já pronta. As interfaces ([terminal](terminal-uno.md) e [servidor web](servidor-web.md)) chamam seus métodos públicos e leem `log`/`ranking()`/`cartas_validas()` para decidir o que mostrar.

| Camada que chama | Método de `JogoUno` |
|---|---|
| Início da partida | `__init__(jogadores)` |
| Tela mostra de quem é a vez | `jogador_da_vez()` |
| Tela mostra a carta do topo | `carta_do_topo()` |
| Tela habilita cartas jogáveis | `cartas_validas(jogador)` |
| Jogador clica/digita uma carta | `jogar_carta(indice, cor_escolhida)` |
| Jogador compra e passa a vez | `comprar_e_passar()` |
| Painel de ranking | `ranking()` |
| Verificar se a partida acabou | `acabou()` |

## Atributos / Estado

```python
class JogoUno:
    # Constantes de classe
    CORES = ["Vermelho", "Azul", "Verde", "Amarelo"]
    VALORES_NORMAIS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    VALORES_ESPECIAIS = ["Pular", "Inverter", "+2"]

    # Estado da instância
    monte_compra: Pilha
    monte_descarte: Pilha
    fila_jogadores: Fila
    cor_atual: str | None     # muda quando um curinga é jogado
    vencedor: Jogador | None
    log: list[str]
```

## Métodos / Funções

```python
def __init__(self, jogadores) -> None

# Preparação (privados)
def _criar_baralho(self) -> None
def _distribuir_cartas(self) -> None
def _virar_primeira_carta(self) -> None

# Consultas (não alteram estado)
def jogador_da_vez(self) -> Jogador
def carta_do_topo(self) -> Carta
def acabou(self) -> bool
def cartas_validas(self, jogador) -> list[int]
def ranking(self) -> list[dict]

# Ações (alteram estado)
def registrar(self, mensagem) -> None
def jogar_carta(self, indice, cor_escolhida=None) -> Carta
def comprar_e_passar(self) -> None

# Auxiliares de ação (privados)
def _aplicar_efeito_no_proximo(self, carta) -> None
def _comprar_carta(self, jogador, quantidade=1) -> None
def _reciclar_descarte(self) -> None
```

## Validações

`jogar_carta` levanta `ValueError` nestes casos:

| Condição | Mensagem |
|---|---|
| Partida já terminou | `"O jogo ja terminou."` |
| Índice fora da faixa da mão | `"Numero de carta invalido."` |
| Carta não combina com o topo | `"A carta {carta} nao pode ser jogada agora."` |
| Curinga sem cor escolhida válida | `"Escolha uma cor para o curinga."` |

`comprar_e_passar` levanta `ValueError("O jogo ja terminou.")` se a partida já tiver vencedor.

## Não Deve Fazer

- Não lê teclado nem imprime nada — qualquer `input()`/`print()` pertence às interfaces ([`uno.py`](terminal-uno.md), [`servidor.py`](servidor-web.md)).
- Não decide a jogada do bot — isso é do módulo [`bot`](bot.md).
- Não serializa para JSON — essa conversão é feita pelo [servidor web](servidor-web.md) chamando `Carta.para_dicionario()`.

## Exemplo de Uso

```python
jogo = JogoUno([Jogador("Matheus"), Jogador("Bot Ana", eh_bot=True)])

if not jogo.acabou():
    indices = jogo.cartas_validas(jogo.jogador_da_vez())
    if indices:
        jogo.jogar_carta(indices[0])
    else:
        jogo.comprar_e_passar()
```

## Links Relacionados

- [`Pilha`](pilha.md), [`Fila`](fila.md), [`ArvoreBinariaBusca`](arvore-binaria-busca.md) — estruturas usadas internamente.
- [`Carta`](carta.md), [`Jogador`](jogador.md) — peças de domínio manipuladas.
- [Regras de Negócio](../regras/regras-de-negocio.md) — quase todas as regras (RN01 a RN13) passam por este componente.
- [Diagrama de Arquitetura](../arquitetura/diagrama.md).

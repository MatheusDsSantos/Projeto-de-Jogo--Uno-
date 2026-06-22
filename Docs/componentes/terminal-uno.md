# Interface `uno.py` (Terminal)

## Objetivo

Permitir jogar UNO direto no terminal, com 2 a 4 jogadores humanos no mesmo teclado.

## Responsabilidades

- Perguntar quantidade de jogadores e seus nomes.
- Exibir o estado do turno (carta do topo, cor atual, mão do jogador).
- Ler a jogada digitada e repassar para [`JogoUno`](jogo-uno.md).
- Mostrar as mensagens novas do `log` após cada turno.
- Exibir o ranking final ao término da partida.

## Papel no Fluxo

`uno.py` é uma das duas interfaces do projeto (a outra é o [servidor web](servidor-web.md)). Ele não tem regras próprias — apenas lê o teclado, chama `JogoUno`/`Jogador`, e imprime o resultado.

| Etapa | Função |
|---|---|
| Configuração inicial | `perguntar_quantidade_jogadores()`, `perguntar_nomes(quantidade)` |
| Laço principal do jogo | `main()` |
| Turno de um jogador | `turno(jogo)` |
| Escolha de cor após curinga | `escolher_cor()` |
| Exibir mensagens novas do log | `mostrar_novidades(jogo, ja_mostradas)` |
| Exibir ranking no fim | `mostrar_ranking(jogo)` |

## Métodos / Funções

```python
def perguntar_quantidade_jogadores() -> int
def perguntar_nomes(quantidade) -> list[str]
def escolher_cor() -> str
def mostrar_novidades(jogo, ja_mostradas) -> int
def mostrar_ranking(jogo) -> None
def turno(jogo) -> None
def main() -> None
```

## Validações

- `perguntar_quantidade_jogadores` repete a pergunta até receber um número entre 2 e 4.
- `turno` trata `ValueError` vindo tanto de erros de digitação (`"invalid literal"`) quanto de regras do motor (mensagens de `JogoUno.jogar_carta`), mostrando a mensagem apropriada ao jogador.

## Não Deve Fazer

- Não implementa nenhuma regra do UNO — toda regra vive em [`JogoUno`](jogo-uno.md).
- Não compartilha estado com o [servidor web](servidor-web.md) — são execuções independentes (`python uno.py` vs. `python servidor.py`).

## Exemplo de Uso

```bash
python uno.py
```

```
Quantos jogadores? (2 a 4): 2
Nome do jogador 1: Matheus
Nome do jogador 2: Ana
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — motor consumido por esta interface.
- [`Jogador`](jogador.md) — criado aqui com `eh_bot=False` (sempre humano no terminal).
- [Servidor Web](servidor-web.md) — interface alternativa, para navegador.

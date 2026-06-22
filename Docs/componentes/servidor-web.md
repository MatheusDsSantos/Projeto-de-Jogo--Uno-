# Interface `servidor.py` (Servidor Web)

## Objetivo

Expor o jogo UNO como uma API JSON sobre HTTP, servindo também os arquivos estáticos do [frontend](interface-web.md), usando apenas a biblioteca padrão do Python (`http.server`).

## Responsabilidades

- Servir os arquivos de `frontend/` (HTML, CSS, JS).
- Manter **uma única partida em memória** (variável global `jogo`).
- Expor rotas que criam a partida, leem o estado, jogam carta, compram carta e executam a jogada do bot.
- Serializar o estado completo do jogo em JSON para o frontend renderizar.
- Proteger o acesso ao estado do jogo contra requisições concorrentes (`trava`, um `threading.Lock`).

## Papel no Fluxo

O `frontend/script.js` consome estas rotas via `fetch`. Cada rota delega a regra de negócio para [`JogoUno`](jogo-uno.md) e devolve o estado atualizado.

| Método | Rota | Corpo | Função acionada |
|---|---|---|---|
| POST | `/api/novo-jogo` | `{"nome": "Matheus", "bots": 2}` | `acao_novo_jogo(dados)` |
| GET | `/api/estado` | — | `estado_do_jogo()` |
| POST | `/api/jogar` | `{"indice": 3, "cor": "Azul"}` | `acao_jogar(dados)` |
| POST | `/api/comprar` | — | `acao_comprar()` |
| POST | `/api/bot-jogar` | — | `acao_bot_jogar()` |

## Atributos / Estado

```python
PORTA = 8000
PASTA_FRONTEND: str            # caminho absoluto até frontend/
NOMES_BOTS = ["Bot Ana", "Bot Beto", "Bot Caio"]

jogo: JogoUno | None            # partida única em memória, módulo-level
trava: threading.Lock           # evita duas requisições alterarem o jogo ao mesmo tempo
```

## Métodos / Funções

```python
def estado_do_jogo() -> dict
def acao_novo_jogo(dados) -> None
def acao_jogar(dados) -> None
def acao_comprar() -> None
def acao_bot_jogar() -> None

class ServidorUno(SimpleHTTPRequestHandler):
    def log_message(self, formato, *args) -> None
    def _responder_json(self, dados, status=200) -> None
    def _ler_corpo_json(self) -> dict
    def do_GET(self) -> None
    def do_POST(self) -> None

def main() -> None
```

## Validações

- `acao_jogar` e `acao_comprar` levantam `ValueError` se não houver jogo em andamento ou se não for a vez do humano (`"Aguarde a sua vez."`).
- `do_POST` captura `ValueError` e `KeyError` e responde com status `400` e `{"erro": "..."}` em vez de quebrar o servidor.
- Rotas não reconhecidas respondem `404` com `{"erro": "Rota nao encontrada."}`.

## Não Deve Fazer

- Não implementa nenhuma regra do UNO — apenas traduz requisições HTTP em chamadas a [`JogoUno`](jogo-uno.md).
- Não persiste a partida em banco de dados ou arquivo — tudo se perde ao reiniciar o processo.
- Não atende mais de uma partida simultânea — a variável `jogo` é única e global.

## Exemplo de Uso

```bash
python servidor.py
# Abra http://localhost:8000 no navegador
```

```http
POST /api/jogar
Content-Type: application/json

{"indice": 2}
```

## Links Relacionados

- [`JogoUno`](jogo-uno.md) — motor por trás de todas as rotas.
- [Interface Web](interface-web.md) — cliente que consome esta API.
- [Diagrama de Arquitetura](../arquitetura/diagrama.md) — fluxo navegador → servidor → motor.

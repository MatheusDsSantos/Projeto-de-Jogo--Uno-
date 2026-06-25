"""
SERVIDOR WEB do jogo UNO.

1. Serve os arquivos da pasta frontend/ (a interface do jogo)
2. Expoe uma API JSON que a interface usa para conversar com o motor
   do jogo (modelo/jogo.py)


Rotas da API:
    POST /api/novo-jogo   {"nome": "Matheus", "bots": 2}
    GET  /api/estado      -> estado atual do jogo
    POST /api/jogar       {"indice": 3, "cor": "Azul"}  (cor so para curinga)
    POST /api/comprar     -> jogador humano compra 1 carta e passa
    POST /api/bot-jogar   -> executa UMA jogada do bot da vez
"""

import json
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from modelo import bot
from modelo.jogador import Jogador
from modelo.jogo import JogoUno

PORTA = 8000
PASTA_FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
NOMES_BOTS = ["Prof me da 10 pfv", "Ou Santo será rebaixado", "Bot Matheus"]

# Uma unica partida em memoria (suficiente para a demonstracao)
jogo = None
trava = threading.Lock()  # Evita duas requisicoes mexerem no jogo ao mesmo tempo


def estado_do_jogo():
    """Monta o dicionario com tudo que a interface precisa exibir."""
    if jogo is None:
        return {"erro": "Nenhum jogo em andamento."}

    jogadores = jogo.fila_jogadores.listar()
    if jogo.vencedor is not None:
        jogadores = jogadores + [jogo.vencedor]

    humano = next((j for j in jogadores if not j.eh_bot), None)
    da_vez = jogo.jogador_da_vez()

    return {
        "jogadores": [
            {
                "nome": j.nome,
                "cartas": j.quantidade_cartas(),
                "bot": j.eh_bot,
                "da_vez": (not jogo.acabou()) and j is da_vez,
            }
            for j in jogadores
        ],
        "mao": [c.para_dicionario() for c in humano.cartas()],
        "jogaveis": jogo.cartas_validas(humano) if not jogo.acabou() else [],
        "topo": jogo.carta_do_topo().para_dicionario(),
        "cor_atual": jogo.cor_atual,
        "monte_compra": jogo.monte_compra.tamanho(),
        "vez_humano": (not jogo.acabou()) and da_vez is humano,
        "vencedor": jogo.vencedor.nome if jogo.vencedor else None,
        "ranking": jogo.ranking(),  # Montado com a Arvore Binaria de Busca
        "log": jogo.log[-30:],
    }


def acao_novo_jogo(dados):
    """Cria uma nova partida: 1 humano + 1 a 3 bots."""
    global jogo

    nome = str(dados.get("nome", "")).strip() or "Jogador"
    quantidade_bots = int(dados.get("bots", 1))
    quantidade_bots = max(1, min(3, quantidade_bots))

    jogadores = [Jogador(nome)]
    for nome_bot in NOMES_BOTS[:quantidade_bots]:
        jogadores.append(Jogador(nome_bot, eh_bot=True))

    jogo = JogoUno(jogadores)
    jogo.registrar(f"Novo jogo: {nome} contra {quantidade_bots} bot(s). Boa sorte!")


def acao_jogar(dados):
    """O jogador humano joga uma carta."""
    if jogo is None or jogo.acabou():
        raise ValueError("Nenhum jogo em andamento.")
    if jogo.jogador_da_vez().eh_bot:
        raise ValueError("Aguarde a sua vez.")

    indice = int(dados.get("indice", -1))
    cor = dados.get("cor")
    jogo.jogar_carta(indice, cor)


def acao_comprar():
    """O jogador humano compra 1 carta e passa a vez."""
    if jogo is None or jogo.acabou():
        raise ValueError("Nenhum jogo em andamento.")
    if jogo.jogador_da_vez().eh_bot:
        raise ValueError("Aguarde a sua vez.")
    jogo.comprar_e_passar()


def acao_bot_jogar():
    """Executa UMA jogada do bot da vez (a interface chama em sequencia)."""
    if jogo is None or jogo.acabou():
        return
    jogador = jogo.jogador_da_vez()
    if not jogador.eh_bot:
        return  # Nao e vez de bot: nada a fazer

    indice, cor = bot.escolher_jogada(jogo, jogador)
    if indice is None:
        jogo.comprar_e_passar()
    else:
        jogo.jogar_carta(indice, cor)


class ServidorUno(SimpleHTTPRequestHandler):
    """Atende as requisicoes: arquivos do frontend + API JSON."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PASTA_FRONTEND, **kwargs)

    def log_message(self, formato, *args):
        pass  # Silencia o log de cada requisicao no terminal

    def _responder_json(self, dados, status=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _ler_corpo_json(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0:
            return {}
        return json.loads(self.rfile.read(tamanho).decode("utf-8"))

    def do_GET(self):
        if self.path == "/api/estado":
            with trava:
                self._responder_json(estado_do_jogo())
        else:
            # Qualquer outro caminho: serve os arquivos de frontend/
            super().do_GET()

###chama as funçoes aqui dependendo da rota requisitada
    def do_POST(self):
        try:
            dados = self._ler_corpo_json()
            with trava:
                if self.path == "/api/novo-jogo":
                    acao_novo_jogo(dados)
                elif self.path == "/api/jogar":
                    acao_jogar(dados)
                elif self.path == "/api/comprar":
                    acao_comprar()
                elif self.path == "/api/bot-jogar":
                    acao_bot_jogar()
                else:
                    self._responder_json({"erro": "Rota nao encontrada."}, 404)
                    return
                self._responder_json(estado_do_jogo())
        except (ValueError, KeyError) as erro:
            self._responder_json({"erro": str(erro)}, 400)


def main():
    servidor = ThreadingHTTPServer(("", PORTA), ServidorUno)
    print("=" * 50)
    print("       SERVIDOR DO JOGO UNO")
    print("=" * 50)
    print(f"\nAbra no navegador:  http://localhost:{PORTA}")
    print("Pressione Ctrl+C para encerrar.\n")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")


if __name__ == "__main__":
    main()

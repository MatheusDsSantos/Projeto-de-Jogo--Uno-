"""
Jogo UNO em Python - INTERFACE DE TERMINAL

Toda a logica do jogo fica em modelo/jogo.py (o motor). Este arquivo
apenas conversa com o usuario pelo teclado.

Estruturas de dados usadas no projeto:
- Pilha (estruturas/pilha.py): montes de compra e descarte
- Fila (estruturas/fila.py): ordem dos turnos
- Lista Encadeada (estruturas/lista_encadeada.py): mao de cada jogador
- Arvore Binaria de Busca (estruturas/arvore.py): ranking dos jogadores

Para jogar no navegador, execute: python servidor.py
"""

from modelo.jogo import JogoUno
from modelo.jogador import Jogador


def perguntar_quantidade_jogadores():
    while True:
        try:
            quantidade = int(input("Quantos jogadores? (2 a 4): "))
            if 2 <= quantidade <= 4:
                return quantidade
            print("Digite um numero entre 2 e 4.")
        except ValueError:
            print("Digite apenas numeros.")


def perguntar_nomes(quantidade):
    nomes = []
    for i in range(quantidade):
        nome = input(f"Nome do jogador {i + 1}: ").strip()
        if not nome:
            nome = f"Jogador {i + 1}"
        nomes.append(nome)
    return nomes


def escolher_cor():
    """Pede ao jogador para escolher uma cor (apos jogar curinga)."""
    print("\nEscolha uma cor:")
    for i, cor in enumerate(JogoUno.CORES):
        print(f"  {i + 1}. {cor}")
    while True:
        try:
            escolha = int(input("  Sua escolha: ")) - 1
            if 0 <= escolha < len(JogoUno.CORES):
                return JogoUno.CORES[escolha]
        except ValueError:
            pass
        print("  Escolha invalida!")


def mostrar_novidades(jogo, ja_mostradas):
    """Imprime as mensagens novas do historico do jogo."""
    for mensagem in jogo.log[ja_mostradas:]:
        print(f"  >> {mensagem}")
    return len(jogo.log)


def mostrar_ranking(jogo):
    """Exibe o ranking montado pela Arvore Binaria de Busca."""
    print("\nRANKING (arvore binaria de busca - percurso em ordem):")
    for posicao, item in enumerate(jogo.ranking(), start=1):
        print(f"  {posicao}o lugar: {item['nome']} ({item['cartas']} cartas)")


def turno(jogo):
    """Executa o turno do jogador da vez."""
    jogador = jogo.jogador_da_vez()

    print("\n" + "=" * 50)
    print(f"Vez de: {jogador.nome}  |  Carta no topo: {jogo.carta_do_topo()}"
          f"  |  Cor: {jogo.cor_atual}")
    print(f"Monte de compra: {jogo.monte_compra.tamanho()} cartas restantes")

    print(f"\nSuas cartas ({jogador.quantidade_cartas()}):")
    for i, carta in enumerate(jogador.cartas()):
        print(f"  {i + 1}. {carta}")

    # Sem carta valida: compra automaticamente e passa a vez
    if not jogo.cartas_validas(jogador):
        print(f"\n{jogador.nome} nao tem cartas validas. Comprando uma carta...")
        jogo.comprar_e_passar()
        return

    # Pede para o jogador escolher uma carta
    while True:
        try:
            print("\nDigite o numero da carta para jogar"
                  " (ou 0 para comprar uma carta):")
            escolha = int(input("  Sua jogada: "))

            if escolha == 0:
                jogo.comprar_e_passar()
                return

            indice = escolha - 1
            cartas = jogador.cartas()

            if indice < 0 or indice >= len(cartas):
                print("  Numero invalido!")
                continue

            cor = None
            if cartas[indice].cor == "Curinga":
                cor = escolher_cor()

            jogo.jogar_carta(indice, cor)
            return

        except ValueError as erro:
            # Erros de regra vindos do motor ou de digitacao
            mensagem = str(erro)
            if "invalid literal" in mensagem:
                print("  Digite apenas numeros!")
            else:
                print(f"  {mensagem}")


def main():
    print("=" * 50)
    print("         CONFIGURACAO DO JOGO UNO")
    print("=" * 50)

    quantidade = perguntar_quantidade_jogadores()
    nomes = perguntar_nomes(quantidade)

    jogadores = [Jogador(nome) for nome in nomes]
    jogo = JogoUno(jogadores)

    print("\n" + "=" * 50)
    print("       BEM-VINDO AO JOGO UNO!")
    print("=" * 50)

    mensagens_mostradas = len(jogo.log)
    while not jogo.acabou():
        turno(jogo)
        mensagens_mostradas = mostrar_novidades(jogo, mensagens_mostradas)

    print("\n" + "=" * 50)
    print(f"  PARABENS, {jogo.vencedor.nome.upper()} VENCEU O JOGO!")
    print("=" * 50)
    mostrar_ranking(jogo)
    print("\nObrigado por jogar!")


if __name__ == "__main__":
    main()

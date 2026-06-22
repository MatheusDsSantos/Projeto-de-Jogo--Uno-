# Escopo do Projeto

## O Sistema Entrega

- Um jogo de UNO completo e jogável, em duas interfaces independentes: terminal (`uno.py`) e navegador (`servidor.py` + `frontend/`).
- Quatro estruturas de dados implementadas do zero (sem usar `list`/`dict` como solução final, exceto internamente): [`Pilha`](../componentes/pilha.md), [`Fila`](../componentes/fila.md), [`ListaEncadeada`](../componentes/lista-encadeada.md) e [`ArvoreBinariaBusca`](../componentes/arvore-binaria-busca.md).
- Regras completas do UNO: cartas numéricas, Pular, Inverter, +2, Curinga e +4, aviso de "UNO!" e condição de vitória — ver [Regras de Negócio](../regras/regras-de-negocio.md).
- Um motor de jogo (`JogoUno`) desacoplado de entrada/saída, reaproveitado pelas duas interfaces.
- Jogadores controlados por computador (bots) com uma estratégia simples de decisão (`modelo/bot.py`).
- Uma API JSON sobre HTTP (`servidor.py`), construída só com a biblioteca padrão do Python (`http.server`), sem frameworks como Flask ou Django.
- Um ranking dos jogadores, ordenado por uma Árvore Binária de Busca em vez de `sort()`.
- Uma interface web com botões informativos (`?`) que explicam, em tempo real, qual estrutura de dados está sendo usada em cada parte da tela.

## Fora do Escopo

- **Persistência:** não há banco de dados nem arquivo de save — o estado da partida vive apenas na memória do processo (`servidor.py`) e se perde ao reiniciar.
- **Múltiplas partidas simultâneas:** o servidor web guarda uma única partida global (`jogo`); não há sessões por usuário nem suporte a múltiplas mesas.
- **Multiplayer em rede real:** todos os jogadores humanos jogam na mesma máquina (terminal) ou o único humano joga contra bots locais (web). Não há comunicação entre navegadores diferentes.
- **Contas de usuário / login:** não existe autenticação; o "nome" do jogador é apenas um texto livre, sem validação de unicidade.
- **Regras de casa (house rules):** não há empilhamento de +2/+4 (jogar +2 sobre +2), nem desafio ("challenge") ao +4, nem regra de "jogar 7" ou "jogar 0" — apenas as regras clássicas básicas.
- **Testes automatizados:** o projeto não inclui suíte de testes; a validação é manual, jogando.
- **Persistência de ranking entre partidas:** o ranking é recalculado a cada chamada de `JogoUno.ranking()`, a partir do estado atual — não existe histórico de partidas anteriores.
- **Empacotamento como aplicativo nativo:** as interfaces são um script de terminal e uma página web; não há instalador nem aplicativo desktop/mobile no código-fonte.

## Decisões de Projeto

| Decisão | Motivo |
|---|---|
| Motor (`JogoUno`) sem `input()`/`print()` | Permitir reaproveitar exatamente a mesma lógica no terminal e na web — ver [Mapa de Componentes](../componentes/README.md#regra-de-ouro). |
| Estruturas de dados implementadas manualmente | Objetivo é didático: mostrar Pilha, Fila, Lista Encadeada e Árvore Binária de Busca funcionando em um caso de uso real, não apenas em teoria. |
| Servidor com `http.server` da biblioteca padrão | Evitar dependências externas — o projeto roda com qualquer instalação padrão do Python 3, sem `pip install`. |
| Uma única partida em memória no servidor | Simplicidade: o projeto é uma demonstração/apresentação, não um produto multiusuário. |
| Frontend sem framework (HTML/CSS/JS puro) | Mesma razão: nenhuma dependência externa, fácil de ler e rodar em qualquer navegador. |
| Erros de regra sempre como `ValueError` | Padroniza o tratamento de erro nas duas interfaces, que só precisam capturar um tipo de exceção. |

## Convenções Padrão

- Toda mensagem voltada ao jogador (log do jogo, erros) é em português.
- Toda nova regra de jogo deve entrar em `modelo/jogo.py` (ou em `Carta`/`Jogador`, se for sobre o dado em si) — nunca nas interfaces.
- Toda nova estrutura de dados genérica entra em `estruturas/`, sem conhecimento das regras do UNO.

## Links Relacionados

- [Roteiro de Implementação](roteiro-de-implementacao.md)
- [Regras de Negócio](../regras/regras-de-negocio.md)
- [Mapa de Componentes](../componentes/README.md)

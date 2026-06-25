/* ============================================================
   UNO - Logica da interface web
   Conversa com o backend Python (servidor.py) via API JSON.
   ============================================================ */

// ---------- Elementos da pagina ----------
const telaInicial = document.getElementById("tela-inicial");
const telaJogo = document.getElementById("tela-jogo");
const campoNome = document.getElementById("campo-nome");
const botaoIniciar = document.getElementById("botao-iniciar");
const botoesBots = document.querySelectorAll(".botao-bot");

const areaOponentes = document.getElementById("area-oponentes");
const cartaTopo = document.getElementById("carta-topo");
const monteCompra = document.getElementById("monte-compra");
const contadorMonte = document.getElementById("contador-monte");
const bolinhaCor = document.getElementById("bolinha-cor");
const avisoVez = document.getElementById("aviso-vez");
const nomeJogador = document.getElementById("nome-jogador");
const maoJogador = document.getElementById("mao-jogador");
const listaRanking = document.getElementById("lista-ranking");
const listaLog = document.getElementById("lista-log");
const botaoReiniciar = document.getElementById("botao-reiniciar");

const modalCor = document.getElementById("modal-cor");
const modalFim = document.getElementById("modal-fim");
const tituloFim = document.getElementById("titulo-fim");
const mensagemFim = document.getElementById("mensagem-fim");
const botaoJogarNovamente = document.getElementById("botao-jogar-novamente");

// ---------- Estado local ----------
let botsEscolhidos = 2;
let meuNome = "";
let indiceCuringa = null;   // guarda a carta curinga aguardando escolha de cor
let rodandoBots = false;    // evita dois loops de bot ao mesmo tempo

const CLASSES_COR = {
  Vermelho: "cor-vermelho",
  Azul: "cor-azul",
  Verde: "cor-verde",
  Amarelo: "cor-amarelo",
  Curinga: "cor-curinga",
};

const CORES_HEX = {
  Vermelho: "#e63946",
  Azul: "#2779d8",
  Verde: "#2a9d4e",
  Amarelo: "#f4c20d",
};

const SIMBOLOS = {
  Pular: "⦸",      // ⦸
  Inverter: "⇄",   // ⇄
  Curinga: "W",
};

// Foto de cada bot (mapeada pelo NOME definido em servidor.py -> NOMES_BOTS).
// Usamos o nome e nao a posicao porque a fila de turnos muda a ordem na tela.
const FOTOS_BOTS = {
  "Prof me da 10 pfv": "img/santos.png",      // bot 1 - escudo do Santos FC
  "Ou Santos será rebaixado": "img/santos.png", // bot 2 - escudo do Santos FC
  "Neymar": "img/neymar.jpg",                  // bot 3 - foto do Neymar
};

// ---------- Comunicacao com o backend ----------

async function chamarApi(rota, corpo) {
  const opcoes = corpo
    ? {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo),
      }
    : { method: rota.startsWith("/api/estado") ? "GET" : "POST" };

  const resposta = await fetch(rota, opcoes);
  const dados = await resposta.json();
  if (!resposta.ok) {
    throw new Error(dados.erro || "Erro no servidor");
  }
  return dados;
}

// ---------- Renderizacao ----------

function simboloDe(valor) {
  return SIMBOLOS[valor] || valor;
}

function criarCartaHTML(carta) {
  const div = document.createElement("div");
  div.className = `carta ${CLASSES_COR[carta.cor]}`;
  const simbolo = simboloDe(carta.valor);
  div.innerHTML = `
    <span class="canto cima">${simbolo}</span>
    <span class="valor">${simbolo}</span>
    <span class="canto baixo">${simbolo}</span>
  `;
  return div;
}

function renderizar(estado) {
  // Oponentes (bots)
  areaOponentes.innerHTML = "";
  estado.jogadores
    .filter((j) => j.bot)
    .forEach((j) => {
      const div = document.createElement("div");
      div.className = "oponente" + (j.da_vez ? " da-vez" : "");
      const miniCartas = Array.from(
        { length: Math.min(j.cartas, 10) },
        () => '<div class="mini-carta"></div>'
      ).join("");
      const foto = FOTOS_BOTS[j.nome];
      const avatar = foto
        ? `<div class="avatar"><img src="${foto}" alt="${j.nome}"></div>`
        : `<div class="avatar">🤖</div>`;
      div.innerHTML = `
        ${avatar}
        <div class="nome">${j.nome}</div>
        <div class="mini-cartas">${miniCartas}</div>
        <div class="contagem">${j.cartas} carta(s)</div>
      `;
      areaOponentes.appendChild(div);
    });

  // Carta do topo do descarte
  const nova = criarCartaHTML(estado.topo);
  cartaTopo.className = nova.className;
  cartaTopo.innerHTML = nova.innerHTML;

  // Monte de compra e cor atual
  contadorMonte.textContent = `${estado.monte_compra} cartas`;
  monteCompra.classList.toggle("desabilitado", !estado.vez_humano);
  bolinhaCor.style.background = CORES_HEX[estado.cor_atual] || "#888";

  // Aviso de quem joga
  if (estado.vencedor) {
    avisoVez.textContent = "";
  } else if (estado.vez_humano) {
    avisoVez.textContent = "✋ Sua vez! Clique em uma carta ou no monte para comprar.";
  } else {
    const daVez = estado.jogadores.find((j) => j.da_vez);
    avisoVez.textContent = daVez ? `${daVez.nome} está jogando...` : "";
  }

  // Mao do jogador humano
  const eu = estado.jogadores.find((j) => !j.bot);
  nomeJogador.textContent = `${eu.nome} — ${estado.mao.length} carta(s)`;
  maoJogador.innerHTML = "";
  estado.mao.forEach((carta, indice) => {
    const div = criarCartaHTML(carta);
    const jogavel = estado.vez_humano && estado.jogaveis.includes(indice);
    div.classList.add(jogavel ? "jogavel" : "bloqueada");
    if (jogavel) {
      div.addEventListener("click", () => jogarCarta(indice, carta));
    }
    maoJogador.appendChild(div);
  });

  // Ranking (montado no backend pela Arvore Binaria de Busca)
  listaRanking.innerHTML = "";
  estado.ranking.forEach((item) => {
    const li = document.createElement("li");
    li.innerHTML = `${item.nome} <span class="qtd">(${item.cartas} cartas)</span>`;
    listaRanking.appendChild(li);
  });

  // Historico
  listaLog.innerHTML = "";
  estado.log.forEach((mensagem) => {
    const li = document.createElement("li");
    li.textContent = mensagem;
    if (mensagem.includes("UNO!") || mensagem.includes("venceu")) {
      li.classList.add("destaque");
    }
    listaLog.appendChild(li);
  });
  listaLog.scrollTop = listaLog.scrollHeight;

  // Fim de jogo
  if (estado.vencedor) {
    const ganhei = estado.vencedor === meuNome;
    tituloFim.textContent = ganhei ? "🎉 Você venceu!" : "😅 Fim de jogo";
    mensagemFim.textContent = ganhei
      ? "Parabéns, você se livrou de todas as cartas!"
      : `${estado.vencedor} venceu a partida.`;
    modalFim.classList.remove("escondida");
  }
}

// ---------- Acoes do jogador ----------

async function jogarCarta(indice, carta) {
  if (carta.cor === "Curinga") {
    indiceCuringa = indice;            // espera a escolha da cor no modal
    modalCor.classList.remove("escondida");
    return;
  }
  await executar(() => chamarApi("/api/jogar", { indice }));
}

async function escolherCor(cor) {
  modalCor.classList.add("escondida");
  const indice = indiceCuringa;
  indiceCuringa = null;
  await executar(() => chamarApi("/api/jogar", { indice, cor }));
}

async function comprarCarta() {
  await executar(() => chamarApi("/api/comprar"));
}

async function executar(acao) {
  try {
    const estado = await acao();
    renderizar(estado);
    rodarBots(estado);
  } catch (erro) {
    avisoVez.textContent = "⚠️ " + erro.message;
  }
}

// Enquanto for a vez de um bot, pede ao backend UMA jogada por vez
// (com uma pausa para dar para acompanhar na tela)
async function rodarBots(estado) {
  if (rodandoBots) return;
  rodandoBots = true;

  try {
    while (estado && !estado.vencedor && !estado.vez_humano) {
      await new Promise((r) => setTimeout(r, 1000));
      estado = await chamarApi("/api/bot-jogar");
      renderizar(estado);
    }
  } catch (erro) {
    avisoVez.textContent = "⚠️ " + erro.message;
  } finally {
    rodandoBots = false;
  }
}

// ---------- Inicio e reinicio ----------

async function iniciarJogo() {
  meuNome = campoNome.value.trim() || "Jogador";
  const estado = await chamarApi("/api/novo-jogo", {
    nome: meuNome,
    bots: botsEscolhidos,
  });
  telaInicial.classList.add("escondida");
  modalFim.classList.add("escondida");
  telaJogo.classList.remove("escondida");
  renderizar(estado);
  rodarBots(estado);
}

botoesBots.forEach((botao) => {
  botao.addEventListener("click", () => {
    botoesBots.forEach((b) => b.classList.remove("selecionado"));
    botao.classList.add("selecionado");
    botsEscolhidos = parseInt(botao.dataset.bots, 10);
  });
});

botaoIniciar.addEventListener("click", iniciarJogo);
campoNome.addEventListener("keydown", (e) => {
  if (e.key === "Enter") iniciarJogo();
});

monteCompra.addEventListener("click", () => {
  if (!monteCompra.classList.contains("desabilitado")) comprarCarta();
});

document.querySelectorAll(".opcao-cor").forEach((botao) => {
  botao.addEventListener("click", () => escolherCor(botao.dataset.cor));
});

botaoJogarNovamente.addEventListener("click", () => {
  modalFim.classList.add("escondida");
  telaJogo.classList.add("escondida");
  telaInicial.classList.remove("escondida");
});

botaoReiniciar.addEventListener("click", () => {
  telaJogo.classList.add("escondida");
  telaInicial.classList.remove("escondida");
});

// ---------- Botões informativos das estruturas ----------

const INFO_ESTRUTURAS = {
  "pilha-compra": {
    icone: "🃏",
    titulo: "Pilha — Monte de Compra",
    tag: "PILHA · LIFO",
    tagClasse: "tag-pilha",
    headerClasse: "info-header-pilha",
    texto:
      "Pensa numa pilha de pratos: você só consegue pegar o de cima, certo? " +
      "O monte de compra funciona exatamente assim. Quando o baralho é formado, " +
      "todas as 108 cartas são empilhadas. Ao comprar, sempre pegamos a do topo — " +
      "esse é o princípio LIFO (Last In, First Out).",
    metodos: [
      { badge: "empurrar(carta)", desc: "adiciona uma carta no topo da pilha" },
      { badge: "retirar()", desc: "remove e devolve a carta do topo ao comprar" },
      { badge: "embaralhar()", desc: "mistura as cartas quando o monte acaba" },
    ],
  },
  "pilha-descarte": {
    icone: "🎴",
    titulo: "Pilha — Monte de Descarte",
    tag: "PILHA · LIFO",
    tagClasse: "tag-pilha",
    headerClasse: "info-header-pilha",
    texto:
      "O descarte também é uma pilha — cada carta jogada vai para o topo, " +
      "e só a última fica visível na mesa. As demais ficam 'soterradas'. " +
      "Quando o monte de compra esgota, o descarte inteiro (menos o topo) " +
      "é reaproveitado, virado e embaralhado de volta.",
    metodos: [
      { badge: "empurrar(carta)", desc: "coloca a carta jogada no topo do descarte" },
      { badge: "ver_topo()", desc: "lê a carta atual para validar a próxima jogada" },
      { badge: "retirar()", desc: "remove cartas para reaproveitar o descarte" },
    ],
  },
  "fila": {
    icone: "🔄",
    titulo: "Fila — Ordem dos Turnos",
    tag: "FILA · FIFO",
    tagClasse: "tag-fila",
    headerClasse: "info-header-fila",
    texto:
      "A ordem de jogo funciona como uma fila de banco: quem chega primeiro, " +
      "é atendido primeiro. A cada rodada, o jogador da vez sai do início " +
      "e entra no final — e assim o ciclo continua. " +
      "A carta Inverter literalmente vira a fila ao contrário, mudando a direção da partida.",
    metodos: [
      { badge: "proximo()", desc: "tira o jogador do início para ele jogar" },
      { badge: "entrar(jogador)", desc: "recoloca o jogador no final da fila" },
      { badge: "inverter()", desc: "inverte a fila quando a carta Inverter é jogada" },
    ],
  },
  "lista": {
    icone: "✋",
    titulo: "Lista Encadeada — Mão do Jogador",
    tag: "LISTA ENCADEADA",
    tagClasse: "tag-lista",
    headerClasse: "info-header-lista",
    texto:
      "As cartas de cada jogador ficam numa lista encadeada: cada carta conhece " +
      "apenas a próxima, formando uma corrente. Não há índice direto — " +
      "para chegar à 5ª carta, percorremos nó por nó desde o início. " +
      "Comprar adiciona no final; jogar percorre até o índice e 'costura' a corrente sem aquele nó.",
    metodos: [
      { badge: "adicionar(carta)", desc: "insere uma carta no final ao comprar" },
      { badge: "remover_por_indice(i)", desc: "percorre e remove a carta que foi jogada" },
      { badge: "listar()", desc: "percorre todos os nós para renderizar a mão na tela" },
    ],
  },
  "abb": {
    icone: "🏆",
    titulo: "Árvore Binária de Busca — Ranking",
    tag: "ÁRVORE BINÁRIA",
    tagClasse: "tag-abb",
    headerClasse: "info-header-abb",
    texto:
      "O ranking não usa sort() — ele é montado com uma Árvore Binária de Busca. " +
      "Cada jogador entra na árvore com chave = número de cartas na mão. " +
      "Quem tem menos vai para a esquerda; quem tem mais, para a direita. " +
      "Percorrer em ordem (esq → raiz → dir) já entrega o ranking pronto, do primeiro ao último.",
    metodos: [
      { badge: "inserir(chave, nome)", desc: "posiciona cada jogador na árvore" },
      { badge: "em_ordem()", desc: "percorre a árvore e retorna o ranking ordenado" },
      { badge: "altura()", desc: "mede o equilíbrio da árvore (uso interno)" },
    ],
  },
};

const modalInfo = document.getElementById("modal-info");
const infoHeader = document.getElementById("info-header");
const infoIcone = document.getElementById("info-icone");
const infoTag = document.getElementById("info-tag");
const infoTitulo = document.getElementById("info-titulo");
const infoTexto = document.getElementById("info-texto");
const infoMetodosLista = document.getElementById("info-metodos-lista");
const infoFechar = document.getElementById("info-fechar");

document.querySelectorAll(".btn-info").forEach((botao) => {
  botao.addEventListener("click", (e) => {
    e.stopPropagation();
    const info = INFO_ESTRUTURAS[botao.dataset.info];
    if (!info) return;

    infoIcone.textContent = info.icone;
    infoHeader.className = `info-header ${info.headerClasse}`;
    infoTag.textContent = info.tag;
    infoTag.className = `tag-estrutura ${info.tagClasse}`;
    infoTitulo.textContent = info.titulo;
    infoTexto.textContent = info.texto;

    infoMetodosLista.innerHTML = "";
    info.metodos.forEach(({ badge, desc }) => {
      const item = document.createElement("div");
      item.className = "info-metodo-item";
      item.innerHTML = `<span class="info-metodo-badge">${badge}</span><span>${desc}</span>`;
      infoMetodosLista.appendChild(item);
    });

    modalInfo.classList.remove("escondida");
  });
});

infoFechar.addEventListener("click", () => modalInfo.classList.add("escondida"));
modalInfo.addEventListener("click", (e) => {
  if (e.target === modalInfo) modalInfo.classList.add("escondida");
});

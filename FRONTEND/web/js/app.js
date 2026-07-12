/**
 * app.js — front-end do LuxeVoyage.
 *
 * SPA sem framework: o menu lateral, os formulários e as tabelas são
 * montados 100% em runtime a partir do que /api/registro devolve (ou seja,
 * a partir de registro.py no backend). Isso espelha a mesma estrutura de
 * navegação que já existe no menu de terminal (main.py -> menu_crud ->
 * menu_dominio -> menu_tabela) e no site Streamlit (app.py).
 */
(() => {
  "use strict";

  const state = {
    registro: null,     // { Dominio: { Tabela: {pk, cols, entidade, plural} } }
    atual: null,         // { dominio, tabela } da tabela em foco
    pagina: { limit: 20, offset: 0 },
    filtro: { campo: "", valor: "" },
    editandoId: null,    // != null enquanto o modal está em modo edição
  };

  const ICONE_DOMINIO = {
    Geografia: "🌎", Parceiros: "🤝", Catalogo: "🧳", Clientes: "👤",
    CRM: "📈", Comercial: "💼", Operacional: "✈️", Auditoria: "🛡️",
  };

  const content = document.getElementById("content");

  // ---------------------------------------------------------------------
  // Bootstrap
  // ---------------------------------------------------------------------
  async function iniciar() {
    ligarEventosGlobais();
    try {
      state.registro = await Api.getRegistro();
      marcarConexao(true);
      montarMenu();
    } catch (e) {
      marcarConexao(false, e.message);
      renderErroCritico(e.message);
      return;
    }
    window.addEventListener("hashchange", rotear);
    if (!location.hash) location.hash = "#/dashboard";
    rotear();
  }

  function marcarConexao(ok, msg) {
    const dot = document.getElementById("conn-dot");
    const label = document.getElementById("conn-label");
    dot.className = "conn-dot " + (ok ? "ok" : "fail");
    label.textContent = ok ? "conectado ao banco" : "sem conexão com a API";
    if (!ok && msg) label.title = msg;
  }

  function renderErroCritico(msg) {
    content.innerHTML = `
      <div class="state-msg error">
        <span class="big">⚠️</span>
        Não foi possível carregar o menu do sistema.<br>${escapeHtml(msg)}
        <br><br>
        <button class="btn btn-primary" onclick="location.reload()">Tentar novamente</button>
      </div>`;
  }

  // ---------------------------------------------------------------------
  // Menu lateral (dinâmico, a partir de state.registro)
  // ---------------------------------------------------------------------
  function montarMenu() {
    const wrap = document.getElementById("nav-dominios");
    wrap.innerHTML = "";

    Object.keys(state.registro).forEach((dominio) => {
      const tabelas = state.registro[dominio];
      const grupo = document.createElement("div");
      grupo.className = "nav-group";
      grupo.dataset.dominio = dominio;

      const toggle = document.createElement("button");
      toggle.className = "nav-group-toggle";
      toggle.innerHTML = `
        <span><span class="nav-ico">${ICONE_DOMINIO[dominio] || "•"}</span>${dominio}</span>
        <span class="chev">▶</span>`;
      toggle.addEventListener("click", () => grupo.classList.toggle("open"));

      const body = document.createElement("div");
      body.className = "nav-group-body";
      Object.keys(tabelas).forEach((tabela) => {
        const a = document.createElement("a");
        a.className = "nav-subitem";
        a.href = `#/dominio/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}`;
        a.textContent = tabela.replace(/_/g, " ");
        a.dataset.dominio = dominio;
        a.dataset.tabela = tabela;
        body.appendChild(a);
      });

      grupo.appendChild(toggle);
      grupo.appendChild(body);
      wrap.appendChild(grupo);
    });
  }

  function atualizarMenuAtivo() {
    document.querySelectorAll(".nav-link").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".nav-subitem").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".nav-group").forEach((el) => el.classList.remove("open"));

    const hash = location.hash;
    if (hash.startsWith("#/dashboard")) {
      document.querySelector('.nav-link[data-route="dashboard"]').classList.add("active");
    } else if (hash.startsWith("#/sql")) {
      document.querySelector('.nav-link[data-route="sql"]').classList.add("active");
    } else if (hash.startsWith("#/dominio/")) {
      const [, , dominio, tabela] = hash.replace("#/", "").split("/");
      const el = document.querySelector(
        `.nav-subitem[data-dominio="${cssEscape(dominio)}"][data-tabela="${cssEscape(tabela)}"]`
      );
      if (el) {
        el.classList.add("active");
        el.closest(".nav-group").classList.add("open");
      }
    }
  }

  function cssEscape(s) { return (window.CSS && CSS.escape) ? CSS.escape(s) : s; }

  // ---------------------------------------------------------------------
  // Roteador (hash-based)
  // ---------------------------------------------------------------------
  function rotear() {
    fecharSidebarMobile();
    const hash = location.hash.replace(/^#\//, "");
    const partes = hash.split("/").filter(Boolean);

    if (partes[0] === "dominio" && partes[1] && partes[2]) {
      state.atual = { dominio: decodeURIComponent(partes[1]), tabela: decodeURIComponent(partes[2]) };
      state.pagina = { limit: 20, offset: 0 };
      state.filtro = { campo: "", valor: "" };
      renderTabela();
    } else if (partes[0] === "sql") {
      renderSql();
    } else {
      renderDashboard();
    }
    atualizarMenuAtivo();
  }

  // ---------------------------------------------------------------------
  // DASHBOARD
  // ---------------------------------------------------------------------
  async function renderDashboard() {
    content.innerHTML = `
      <div class="page-head">
        <p class="page-eyebrow">Painel geral</p>
        <h1 class="page-title">🧳 LuxeVoyage</h1>
        <p class="page-sub">Visão geral do banco de dados. Use o menu à esquerda para navegar pelos domínios ou rodar uma consulta SQL livre.</p>
      </div>

      <div class="panel-grid" style="margin-bottom: 24px; grid-template-columns: 1fr;">
        <div class="panel" style="display: flex; gap: 12px; align-items: center; justify-content: flex-start; padding: 20px;">
            <div style="flex: 1">
              <h3 style="margin: 0 0 4px 0">Ferramentas de Análise</h3>
              <p style="margin: 0; font-size: 13px; color: var(--ink-soft)">Gere gráficos, exporte os dados tratados ou envie o relatório atualizado por e-mail para a diretoria.</p>
            </div>
            <button class="btn btn-gold" id="btn-rodar-analise" style="white-space: nowrap">
               📊 Gerar Gráficos e CSVs
            </button>
            <button class="btn btn-primary" id="btn-enviar-email" style="white-space: nowrap">
               📧 Enviar Relatório por E-mail
            </button>
        </div>
      </div>

      <div class="metric-grid" id="metric-grid">
        ${["Clientes","Pacotes","Parceiros","Viagens"].map(() => `
          <div class="metric-card"><div class="skeleton-row" style="width:60%"></div>
          <div class="skeleton-row" style="width:40%;height:26px;margin-top:10px"></div></div>`).join("")}
      </div>
      <div class="panel-grid">
        <div class="panel">
          <h3>Oportunidades por estágio do funil</h3>
          <div id="chart-funil"><div class="skeleton-row" style="width:100%"></div></div>
        </div>
        <div class="panel">
          <h3>Viagens por status</h3>
          <div id="chart-viagens"><div class="skeleton-row" style="width:100%"></div></div>
        </div>
      </div>
      <div id="graficos-gerados" class="panel-grid" style="margin-top: 24px; display: grid; gap: 24px; grid-template-columns: repeat(2, 1fr);"></div>`;

    document.getElementById("btn-rodar-analise").addEventListener("click", async (e) => {
      const btn = e.target.closest("button");
      btn.disabled = true;
      btn.textContent = "⏳ Processando...";
      try {
        const res = await Api.rodarAnalise();
        toast(res.mensagem, "ok");
        loadGraficos();
      } catch (err) {
        toast(err.message, "err");
      } finally {
        btn.disabled = false;
        btn.innerHTML = "📊 Gerar Gráficos e CSVs";
      }
    });

    document.getElementById("btn-enviar-email").addEventListener("click", async (e) => {
      const btn = e.target.closest("button");
      btn.disabled = true;
      btn.textContent = "⏳ Enviando...";
      try {
        const res = await Api.enviarEmail();
        toast(res.mensagem, "ok");
      } catch (err) {
        toast(err.message, "err");
      } finally {
        btn.disabled = false;
        btn.innerHTML = "📧 Enviar Relatório por E-mail";
      }
    });

    try {
      const dados = await Api.getDashboard();
      renderMetricas(dados.metricas);
      renderBarChart("chart-funil", dados.funil);
      renderBarChart("chart-viagens", dados.viagens_status);
    } catch (e) {
      toast(e.message, "err");
      document.getElementById("metric-grid").innerHTML =
        `<div class="state-msg error">Não foi possível carregar as métricas: ${escapeHtml(e.message)}</div>`;
    }
    
    async function loadGraficos() {
      try {
        const files = await Api.listarGraficos();
        const container = document.getElementById("graficos-gerados");
        if (files && files.length > 0) {
          container.innerHTML = files.map(f => `
            <div class="panel" style="padding: 16px; text-align: center;">
              <h4 style="margin: 0 0 12px 0; color: var(--ink-soft); font-family: var(--font-body); text-transform: capitalize;">${f.replace('.png', '').replace(/_/g, ' ')}</h4>
              <img src="/saida/graficos/${f}" style="max-width: 100%; height: auto; border-radius: var(--radius-sm);" alt="${f}" />
            </div>
          `).join("");
        } else {
          container.innerHTML = `<div class="panel" style="grid-column: 1 / -1;"><p class="empty-note">Nenhum gráfico gerado ainda. Clique em "Gerar Gráficos e CSVs".</p></div>`;
        }
      } catch(e) {
        console.error("Erro ao carregar gráficos", e);
      }
    }
    
    loadGraficos();
  }

    function renderMetricas(metricas) {
    const grid = document.getElementById("metric-grid");
    grid.innerHTML = Object.entries(metricas).map(([rotulo, valor]) => `
      <div class="metric-card">
        <div class="metric-label">${escapeHtml(rotulo)}</div>
        <div class="metric-value">${Number(valor).toLocaleString("pt-BR")}</div>
      </div>`).join("");
  }

  function renderBarChart(containerId, linhas) {
    const el = document.getElementById(containerId);
    if (!linhas || linhas.length === 0) {
      el.innerHTML = `<p class="empty-note">Nenhum registro cadastrado ainda.</p>`;
      return;
    }
    const max = Math.max(...linhas.map((l) => Number(l.total) || 0), 1);
    el.innerHTML = linhas.map((l) => {
      const pct = Math.max(4, Math.round((Number(l.total) / max) * 100));
      return `
        <div class="bar-row">
          <div class="bar-label" title="${escapeHtml(String(l.rotulo))}">${escapeHtml(String(l.rotulo))}</div>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          <div class="bar-value">${l.total}</div>
        </div>`;
    }).join("");
  }

  // ---------------------------------------------------------------------
  // TABELA (listar / buscar / paginação)
  // ---------------------------------------------------------------------
  function infoAtual() {
    const { dominio, tabela } = state.atual;
    return { dominio, tabela, info: state.registro[dominio][tabela] };
  }

  async function renderTabela() {
    const { dominio, tabela, info } = infoAtual();
    const colunas = [info.pk, ...info.cols];

    content.innerHTML = `
      <div class="page-head">
        <p class="page-eyebrow">${escapeHtml(dominio)}</p>
        <h1 class="page-title">${tabela.replace(/_/g, " ")}</h1>
        <p class="page-sub">Chave primária: <code>${escapeHtml(info.pk)}</code> · ${info.cols.length} coluna(s) editável(is)</p>
      </div>

      <div class="toolbar">
        <form class="search-form" id="search-form">
          <select id="search-campo">
            <option value="">Buscar por campo…</option>
            ${colunas.map((c) => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join("")}
          </select>
          <span class="divider"></span>
          <input type="text" id="search-valor" placeholder="valor exato">
          <button class="btn btn-ghost btn-sm" type="submit">Buscar</button>
          <button class="btn btn-ghost btn-sm" type="button" id="search-limpar">Limpar</button>
        </form>
        <button class="btn btn-gold" id="btn-novo">+ Novo registro</button>
      </div>

      <div class="table-wrap">
        <div id="tabela-body">
          <div class="state-msg">Carregando registros…</div>
        </div>
        <div class="table-footer" id="table-footer" style="display:none">
          <span id="footer-info"></span>
          <div class="pager">
            <button class="btn btn-ghost btn-sm" id="btn-anterior">‹ Anterior</button>
            <button class="btn btn-ghost btn-sm" id="btn-proximo">Próxima ›</button>
          </div>
        </div>
      </div>`;

    document.getElementById("btn-novo").addEventListener("click", () => abrirModal("criar"));
    document.getElementById("search-form").addEventListener("submit", (ev) => {
      ev.preventDefault();
      state.filtro.campo = document.getElementById("search-campo").value;
      state.filtro.valor = document.getElementById("search-valor").value;
      state.pagina.offset = 0;
      carregarRegistros();
    });
    document.getElementById("search-limpar").addEventListener("click", () => {
      state.filtro = { campo: "", valor: "" };
      state.pagina.offset = 0;
      renderTabela();
    });
    document.getElementById("btn-anterior").addEventListener("click", () => {
      state.pagina.offset = Math.max(0, state.pagina.offset - state.pagina.limit);
      carregarRegistros();
    });
    document.getElementById("btn-proximo").addEventListener("click", () => {
      state.pagina.offset += state.pagina.limit;
      carregarRegistros();
    });

    await carregarRegistros();
  }

  async function carregarRegistros() {
    const { dominio, tabela, info } = infoAtual();
    const body = document.getElementById("tabela-body");
    const footer = document.getElementById("table-footer");
    body.innerHTML = `<div class="state-msg">Carregando registros…</div>`;
    footer.style.display = "none";

    try {
      const resp = await Api.listar(dominio, tabela, {
        limit: state.pagina.limit,
        offset: state.pagina.offset,
        campo: state.filtro.campo,
        valor: state.filtro.valor,
      });
      renderLinhasTabela(resp.registros, info);

      const usandoFiltro = !!(state.filtro.campo && state.filtro.valor);
      footer.style.display = "flex";
      document.getElementById("footer-info").textContent = usandoFiltro
        ? `${resp.total} resultado(s) para ${state.filtro.campo} = "${state.filtro.valor}"`
        : `Mostrando ${resp.registros.length} registro(s) · offset ${state.pagina.offset}`;
      document.getElementById("btn-anterior").disabled = usandoFiltro || state.pagina.offset === 0;
      document.getElementById("btn-proximo").disabled = usandoFiltro || resp.registros.length < state.pagina.limit;
    } catch (e) {
      body.innerHTML = `<div class="state-msg error"><span class="big">⚠️</span>${escapeHtml(e.message)}</div>`;
      toast(e.message, "err");
    }
  }

  function renderLinhasTabela(registros, info) {
    const body = document.getElementById("tabela-body");
    const colunas = [info.pk, ...info.cols];

    if (!registros || registros.length === 0) {
      body.innerHTML = `<div class="state-msg"><span class="big">🗂️</span>Nenhum registro encontrado.</div>`;
      return;
    }

    const thead = `<thead><tr>${colunas.map((c) => `<th>${escapeHtml(c)}</th>`).join("")}<th>Ações</th></tr></thead>`;
    const tbody = `<tbody>${registros.map((r) => `
      <tr>
        ${colunas.map((c, i) => `<td class="${i === 0 ? "pk-cell" : ""}">${formatarCelula(c, r[c])}</td>`).join("")}
        <td class="actions-cell">
          <button class="btn btn-ghost btn-sm" data-editar="${escapeHtml(String(r[info.pk]))}">Editar</button>
          <button class="btn btn-danger btn-sm" data-excluir="${escapeHtml(String(r[info.pk]))}">Excluir</button>
        </td>
      </tr>`).join("")}</tbody>`;

    body.innerHTML = `<table class="data-table">${thead}${tbody}</table>`;

    body.querySelectorAll("[data-editar]").forEach((btn) =>
      btn.addEventListener("click", () => abrirModal("editar", btn.dataset.editar)));
    body.querySelectorAll("[data-excluir]").forEach((btn) =>
      btn.addEventListener("click", () => confirmarExclusao(btn.dataset.excluir)));
  }

  // Colunas monetárias (mas NÃO "numero_parcela"/"total_parcelas", que são contagens)
  const RE_MONEY = /(valor|preco|preço)/i;
  // Colunas booleanas conhecidas do modelo (0/1 vindos do MySQL)
  const RE_BOOLEAN_COL = /^(obrigatorio|ativo|confirmado)$/i;
  // Data (YYYY-MM-DD) ou data+hora ISO (YYYY-MM-DDTHH:MM:SS / "YYYY-MM-DD HH:MM:SS")
  const RE_DATA_ISO = /^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?)?/;
  // VARBINARY/BLOB (ex.: colunas *_criptografado) — o backend serializa como "0x...hex"
  const RE_BINARIO_HEX = /^0x[0-9a-f]+$/i;

  function formatarCelula(coluna, valor) {
    if (valor === null || valor === undefined || valor === "") return `<span style="color:var(--ink-faint)">—</span>`;

    if (/status/i.test(coluna)) return badgeStatus(String(valor));

    if (typeof valor === "string" && RE_BINARIO_HEX.test(valor)) {
      const bytesTotal = (valor.length - 2) / 2;
      return `<span class="badge badge-blue" title="${escapeHtml(valor)}">🔒 binário (${bytesTotal}B)</span>`;
    }

    if (RE_BOOLEAN_COL.test(coluna) && (valor === 0 || valor === 1 || valor === "0" || valor === "1")) {
      const sim = Number(valor) === 1;
      return `<span class="badge ${sim ? "badge-green" : "badge-red"}">${sim ? "Sim" : "Não"}</span>`;
    }

    if (RE_MONEY.test(coluna) && !isNaN(parseFloat(valor)) && isFinite(valor)) {
      const numero = Number(valor);
      return `<span title="${escapeHtml(String(valor))}">${numero.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}</span>`;
    }

    if (typeof valor === "string" && RE_DATA_ISO.test(valor)) {
      const temHora = /\d{2}:\d{2}/.test(valor);
      const d = new Date(valor.replace(" ", "T"));
      if (!isNaN(d.getTime())) {
        const formatado = temHora
          ? d.toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit" })
          : d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric", timeZone: "UTC" });
        return `<span title="${escapeHtml(valor)}">${formatado}</span>`;
      }
    }

    const texto = String(valor);
    // título com o valor completo: colunas de texto longo (comentários, endereços, nomes)
    // ficam truncadas com "…" no CSS, mas o valor inteiro aparece ao passar o mouse.
    return `<span title="${escapeHtml(texto)}">${escapeHtml(texto)}</span>`;
  }

  function badgeStatus(valor) {
    const v = valor.toLowerCase();
    let classe = "badge-blue";
    if (/(ativ|aprovad|pago|confirmad|conclu[ií]d|dispon[ií]vel)/.test(v)) classe = "badge-green";
    else if (/(inativ|cancelad|recusad|atrasad|bloquead|rejeitad)/.test(v)) classe = "badge-red";
    else if (/(pendente|aguard|em anál|rascunho)/.test(v)) classe = "badge-gold";
    return `<span class="badge ${classe}">${escapeHtml(valor)}</span>`;
  }

  async function confirmarExclusao(id) {
    const { dominio, tabela } = infoAtual();
    if (!confirm(`Confirma a exclusão do registro ${id}? Essa ação não pode ser desfeita.`)) return;
    try {
      const resp = await Api.deletar(dominio, tabela, id);
      toast(resp.mensagem || "Registro excluído.", "ok");
      carregarRegistros();
    } catch (e) {
      toast(e.message, "err");
    }
  }

  // ---------------------------------------------------------------------
  // MODAL — criar / editar (formulário dinâmico a partir de info.cols)
  // ---------------------------------------------------------------------
  const modalOverlay = document.getElementById("modal-overlay");
  const modalForm = document.getElementById("modal-form");
  const modalTitle = document.getElementById("modal-title");

  async function abrirModal(modo, id = null) {
    const { dominio, tabela, info } = infoAtual();
    state.editandoId = modo === "editar" ? id : null;
    modalTitle.textContent = modo === "editar" ? `Editar ${tabela.replace(/_/g, " ")} #${id}` : `Novo registro — ${tabela.replace(/_/g, " ")}`;

    let valoresAtuais = {};
    if (modo === "editar") {
      modalForm.innerHTML = `<div class="state-msg">Carregando registro…</div>`;
      modalOverlay.classList.add("open");
      try {
        valoresAtuais = await Api.buscarPorId(dominio, tabela, id);
      } catch (e) {
        toast(e.message, "err");
        fecharModal();
        return;
      }
    }

    modalForm.innerHTML = `
      <div class="form-error" id="form-error"></div>
      ${modo === "editar" ? `
        <div class="field">
          <label>${escapeHtml(info.pk)}</label>
          <input type="text" value="${escapeHtml(String(valoresAtuais[info.pk] ?? id))}" disabled>
        </div>` : ""}
      ${info.cols.map((c) => {
        const valorAtual = valoresAtuais[c];
        const ehBinario = modo === "editar" && typeof valorAtual === "string" && RE_BINARIO_HEX.test(valorAtual);
        if (ehBinario) {
          return `
            <div class="field">
              <label for="f-${c}">${escapeHtml(c)}</label>
              <input type="text" id="f-${c}" name="${escapeHtml(c)}" value="🔒 dado binário/criptografado" disabled data-binario="1">
              <span class="hint">Esse campo guarda um valor binário criptografado e não pode ser editado por aqui.</span>
            </div>`;
        }
        return `
        <div class="field">
          <label for="f-${c}">${escapeHtml(c)}</label>
          <input type="text" id="f-${c}" name="${escapeHtml(c)}"
                 value="${escapeHtml(valorAtual !== undefined && valorAtual !== null ? String(valorAtual) : "")}"
                 placeholder="${modo === "editar" ? "deixe em branco para não alterar" : ""}">
        </div>`;
      }).join("")}
      <div class="modal-actions">
        <button type="button" class="btn btn-ghost" id="btn-cancelar-modal">Cancelar</button>
        <button type="submit" class="btn btn-primary">${modo === "editar" ? "Salvar alterações" : "Criar registro"}</button>
      </div>`;

    document.getElementById("btn-cancelar-modal").addEventListener("click", fecharModal);
    modalForm.onsubmit = (ev) => { ev.preventDefault(); salvarModal(modo, id); };
    modalOverlay.classList.add("open");
    const primeiro = modalForm.querySelector("input:not([disabled])");
    if (primeiro) primeiro.focus();
  }

  async function salvarModal(modo, id) {
    const { dominio, tabela, info } = infoAtual();
    const dados = {};
    info.cols.forEach((c) => {
      const campo = document.getElementById(`f-${c}`);
      if (campo.dataset.binario === "1") return; // não reenviar valor binário/criptografado
      dados[c] = campo.value.trim();
    });

    const erroBox = document.getElementById("form-error");
    erroBox.classList.remove("show");

    try {
      if (modo === "editar") {
        const resp = await Api.atualizar(dominio, tabela, id, dados);
        toast(resp.mensagem || "Registro atualizado.", "ok");
      } else {
        const resp = await Api.criar(dominio, tabela, dados);
        toast(resp.mensagem || "Registro criado.", "ok");
      }
      fecharModal();
      carregarRegistros();
    } catch (e) {
      erroBox.textContent = e.message;
      erroBox.classList.add("show");
    }
  }

  function fecharModal() {
    modalOverlay.classList.remove("open");
    modalForm.innerHTML = "";
    state.editandoId = null;
  }

  // ---------------------------------------------------------------------
  // CONSULTA SQL LIVRE
  // ---------------------------------------------------------------------
  function renderSql() {
    content.innerHTML = `
      <div class="page-head">
        <p class="page-eyebrow">Ferramentas</p>
        <h1 class="page-title">🛠️ Consulta SQL livre</h1>
        <p class="page-sub">Por segurança, apenas comandos <strong>SELECT</strong> são permitidos aqui — igual ao modo 9 do menu de terminal.</p>
      </div>
      <div class="sql-box">
        <textarea id="sql-input" placeholder="SELECT * FROM Cliente LIMIT 10"></textarea>
        <div class="sql-actions">
          <span class="sql-hint">Ctrl/Cmd + Enter executa a consulta</span>
          <button class="btn btn-gold" id="btn-executar">▶ Executar</button>
        </div>
      </div>
      <div class="table-wrap" id="sql-result-wrap" style="display:none">
        <div id="sql-result"></div>
      </div>`;

    const input = document.getElementById("sql-input");
    const executar = async () => {
      const query = input.value.trim();
      const wrap = document.getElementById("sql-result-wrap");
      const result = document.getElementById("sql-result");
      if (!query) return;
      wrap.style.display = "block";
      result.innerHTML = `<div class="state-msg">Executando…</div>`;
      try {
        const resp = await Api.consultaSql(query);
        if (!resp.registros || resp.registros.length === 0) {
          result.innerHTML = `<div class="state-msg">Consulta executada, nenhum resultado retornado.</div>`;
          return;
        }
        const colunas = Object.keys(resp.registros[0]);
        result.innerHTML = `
          <table class="data-table">
            <thead><tr>${colunas.map((c) => `<th>${escapeHtml(c)}</th>`).join("")}</tr></thead>
            <tbody>${resp.registros.map((r) => `<tr>${colunas.map((c) => `<td>${formatarCelula(c, r[c])}</td>`).join("")}</tr>`).join("")}</tbody>
          </table>
          <div class="table-footer"><span>${resp.total} registro(s)</span><span></span></div>`;
      } catch (e) {
        result.innerHTML = `<div class="state-msg error"><span class="big">⚠️</span>${escapeHtml(e.message)}</div>`;
      }
    };
    document.getElementById("btn-executar").addEventListener("click", executar);
    input.addEventListener("keydown", (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === "Enter") executar();
    });
  }

  // ---------------------------------------------------------------------
  // Utilidades: toasts, escape, eventos globais, sidebar mobile
  // ---------------------------------------------------------------------
  function toast(msg, tipo = "ok") {
    const stack = document.getElementById("toast-stack");
    const el = document.createElement("div");
    el.className = `toast ${tipo}`;
    el.textContent = msg;
    stack.appendChild(el);
    setTimeout(() => el.remove(), 4200);
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function ligarEventosGlobais() {
    document.getElementById("modal-close").addEventListener("click", fecharModal);
    modalOverlay.addEventListener("click", (ev) => { if (ev.target === modalOverlay) fecharModal(); });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") fecharModal(); });

    document.getElementById("mobile-toggle").addEventListener("click", () => {
      document.getElementById("sidebar").classList.toggle("open");
    });
  }

  function fecharSidebarMobile() {
    document.getElementById("sidebar").classList.remove("open");
  }

  document.addEventListener("DOMContentLoaded", iniciar);
})();

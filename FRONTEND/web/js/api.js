/**
 * api.js — camada única de comunicação com o backend Flask (api_server.py).
 * Nenhum outro arquivo JS faz fetch() diretamente; tudo passa por aqui,
 * pra manter as URLs da API centralizadas em um só lugar.
 */
const Api = (() => {
  // Mesma origem do index.html por padrão (o Flask serve os dois juntos).
  // Se você abrir o index.html direto de um servidor estático separado,
  // troque a linha abaixo pelo endereço da API, ex: "http://localhost:5000"
  const BASE_URL = "";

  async function _request(path, options = {}) {
    let resposta;
    try {
      resposta = await fetch(BASE_URL + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });
    } catch (redeErro) {
      throw new Error("Não foi possível falar com o servidor. Ele está rodando? (python api_server.py)");
    }

    let corpo = null;
    try { corpo = await resposta.json(); } catch (_) { /* resposta sem corpo */ }

    if (!resposta.ok) {
      const msg = (corpo && corpo.erro) ? corpo.erro : `Erro HTTP ${resposta.status}`;
      throw new Error(msg);
    }
    return corpo;
  }

  return {
    /** Estrutura de domínios/tabelas (fonte: registro.py) */
    getRegistro: () => _request("/api/registro"),

    /** Métricas + gráficos da home */
    getDashboard: () => _request("/api/dashboard"),

    /** Lista paginada, ou busca por campo=valor se informados */
    listar: (dominio, tabela, { limit = 20, offset = 0, campo, valor } = {}) => {
      const params = new URLSearchParams();
      if (campo && valor !== undefined && valor !== "") {
        params.set("campo", campo);
        params.set("valor", valor);
      } else {
        params.set("limit", limit);
        params.set("offset", offset);
      }
      return _request(`/api/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}?${params.toString()}`);
    },

    buscarPorId: (dominio, tabela, id) =>
      _request(`/api/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}/${encodeURIComponent(id)}`),

    criar: (dominio, tabela, dados) =>
      _request(`/api/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}`, {
        method: "POST",
        body: JSON.stringify(dados),
      }),

    atualizar: (dominio, tabela, id, dados) =>
      _request(`/api/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}/${encodeURIComponent(id)}`, {
        method: "PUT",
        body: JSON.stringify(dados),
      }),

    deletar: (dominio, tabela, id) =>
      _request(`/api/${encodeURIComponent(dominio)}/${encodeURIComponent(tabela)}/${encodeURIComponent(id)}`, {
        method: "DELETE",
      }),

    consultaSql: (query) =>
      _request("/api/sql", { method: "POST", body: JSON.stringify({ query }) }),

    rodarAnalise: () =>
      _request("/api/ferramentas/analise", { method: "POST" }),

    enviarEmail: () =>
      _request("/api/ferramentas/email", { method: "POST" }),

    listarGraficos: () =>
      _request("/api/graficos"),
  };
})();

"""
api_server.py — Backend REST (Flask) do site LuxeVoyage.

Reaproveita 100% da camada de dados que já existe no projeto (TEST/*,
utils.py, registro.py). Não duplica nenhuma regra de negócio: chama
exatamente as mesmas funções que o menu de terminal (main.py) e o site
Streamlit (app.py) já usam — só expõe tudo como JSON, para ser consumido
pelo front-end estático em FRONTEND/web/ (HTML + CSS + JS puro,
sem frameworks).

Como rodar (a partir da pasta SRC/):

    pip install -r requirements.txt
    python api_server.py

Depois abra http://localhost:5000 no navegador. O menu do site
(domínios -> tabelas) é montado dinamicamente a partir de registro.py,
então qualquer tabela nova cadastrada lá aparece no site automaticamente,
sem precisar tocar em nenhum arquivo de front-end.
"""
import os
import sys
import pathlib
import decimal
import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask.json.provider import DefaultJSONProvider

# --- bootstrap de caminho (igual ao main.py) --------------------------------
_RAIZ_PROJETO = pathlib.Path(__file__).resolve().parent.parent
_PASTA_TEST = _RAIZ_PROJETO / "TEST"
if str(_PASTA_TEST) not in sys.path:
    sys.path.insert(0, str(_PASTA_TEST))
# -----------------------------------------------------------------------------

from utils import execute_query          # noqa: E402
from registro import REGISTRO            # noqa: E402

_FRONTEND_WEB = _RAIZ_PROJETO / "FRONTEND" / "web"
_PASTA_SAIDA = _RAIZ_PROJETO / "SRC" / "saida" / "graficos"


# ---------------------------------------------------------------------------
# Serialização JSON customizada.
#
# O conector do MySQL devolve tipos Python que o Flask NÃO sabe transformar
# em JSON por padrão:
#   - colunas DECIMAL/NUMERIC (valor_total, valor_estimado, ...) viram
#     decimal.Decimal
#   - colunas DATE/DATETIME/TIMESTAMP viram datetime.date / datetime.datetime
#   - colunas TIME viram datetime.timedelta
#
# Sem isso, qualquer tabela com esse tipo de coluna quebra (erro 500) ou
# devolve o registro incompleto/mal formatado pro front. Este provider
# resolve isso na raiz, pra qualquer endpoint da API.
# ---------------------------------------------------------------------------
class JSONProviderLuxeVoyage(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # número puro (o front formata como moeda/percentual conforme a coluna)
            return float(obj)
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        if isinstance(obj, datetime.timedelta):
            return str(obj)
        if isinstance(obj, (bytes, bytearray)):
            # colunas VARBINARY/BLOB (ex.: Cliente.*_criptografado). O conteúdo é
            # binário/criptografado, então não faz sentido decodificar como texto —
            # mostramos em hexadecimal, igual a um cliente SQL, só pra não quebrar o JSON.
            return "0x" + bytes(obj).hex()
        return super().default(obj)


app = Flask(__name__, static_folder=str(_FRONTEND_WEB), static_url_path="")
app.json_provider_class = JSONProviderLuxeVoyage
app.json = app.json_provider_class(app)


# ---------------------------------------------------------------------------
# CORS simples (sem depender de flask-cors) — só pra permitir abrir o
# index.html direto de outra origem/porta durante o desenvolvimento.
# ---------------------------------------------------------------------------
@app.after_request
def _liberar_cors(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return resposta


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _info_ou_none(dominio, tabela):
    dominio_dict = REGISTRO.get(dominio)
    if dominio_dict is None:
        return None
    return dominio_dict.get(tabela)


def _erro(mensagem, status=400):
    return jsonify({"erro": mensagem}), status



@app.route("/saida/graficos/<path:filename>")
def serve_grafico(filename):
    return send_from_directory(str(_PASTA_SAIDA), filename)

@app.route("/api/graficos")
def list_graficos():
    if not _PASTA_SAIDA.exists():
        return jsonify([])
    files = [f.name for f in _PASTA_SAIDA.iterdir() if f.is_file() and f.name.endswith(".png")]
    return jsonify(files)

# ---------------------------------------------------------------------------
# Front-end estático (HTML / CSS / JS)

# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory(str(_FRONTEND_WEB), "index.html")


# ---------------------------------------------------------------------------
# Estrutura do menu — domínio -> tabela -> pk/colunas.
# É o mesmo REGISTRO usado por main.py e app.py: fonte única de verdade.
# O front-end monta o menu lateral e os formulários inteiramente a partir
# deste endpoint, então nunca fica fora de sincronia com o backend.
# ---------------------------------------------------------------------------
@app.route("/api/registro")
def api_registro():
    estrutura = {}
    for dominio, tabelas in REGISTRO.items():
        estrutura[dominio] = {}
        for nome_tabela, info in tabelas.items():
            estrutura[dominio][nome_tabela] = {
                "pk": info["pk"],
                "cols": info["cols"],
                "entidade": info["entidade"],
                "plural": info["plural"],
            }
    return jsonify(estrutura)


# ---------------------------------------------------------------------------
# Dashboard (home) — mesmas métricas/gráficos do home_page.py do Streamlit.
# ---------------------------------------------------------------------------
@app.route("/api/dashboard")
def api_dashboard():
    def contar(tabela):
        try:
            r = execute_query(f"SELECT COUNT(*) AS total FROM {tabela}", fetch="one")
            return r["total"] if r else 0
        except Exception:
            return 0

    metricas = {
        "Clientes": contar("Cliente"),
        "Pacotes": contar("Pacote"),
        "Parceiros": contar("Parceiros"),
        "Viagens": contar("Viagem"),
    }

    try:
        funil = execute_query(
            "SELECT estagio_funil AS rotulo, COUNT(*) AS total "
            "FROM Oportunidade_CRM GROUP BY estagio_funil",
            fetch="all",
        ) or []
    except Exception:
        funil = []

    try:
        viagens_status = execute_query(
            "SELECT status_viagem AS rotulo, COUNT(*) AS total "
            "FROM Viagem GROUP BY status_viagem",
            fetch="all",
        ) or []
    except Exception:
        viagens_status = []

    return jsonify({
        "metricas": metricas,
        "funil": funil,
        "viagens_status": viagens_status,
    })


# ---------------------------------------------------------------------------
# CRUD genérico — funciona para QUALQUER tabela cadastrada em REGISTRO,
# chamando as mesmas funções (criar_/listar_/buscar_/atualizar_/deletar_)
# que já existem em TEST/<dominio>/<tabela>.py.
# ---------------------------------------------------------------------------
@app.route("/api/<dominio>/<tabela>", methods=["GET"])
def api_listar(dominio, tabela):
    info = _info_ou_none(dominio, tabela)
    if not info:
        return _erro("Domínio/tabela não encontrado.", 404)

    campo = request.args.get("campo")
    valor = request.args.get("valor")

    try:
        if campo and valor not in (None, ""):
            colunas_validas = [info["pk"]] + info["cols"]
            if campo not in colunas_validas:
                return _erro(f"Campo inválido. Use um de: {', '.join(colunas_validas)}")
            funcao = getattr(info["mod"], f"buscar_{info['plural']}_por_campo")
            registros = funcao(campo, valor)
        else:
            limit = int(request.args.get("limit", 20))
            offset = int(request.args.get("offset", 0))
            funcao = getattr(info["mod"], f"listar_{info['plural']}")
            registros = funcao(limit=limit, offset=offset)
        return jsonify({"registros": registros, "total": len(registros)})
    except Exception as e:
        return _erro(str(e), 500)


@app.route("/api/<dominio>/<tabela>/<id_valor>", methods=["GET"])
def api_buscar_por_id(dominio, tabela, id_valor):
    info = _info_ou_none(dominio, tabela)
    if not info:
        return _erro("Domínio/tabela não encontrado.", 404)
    try:
        funcao = getattr(info["mod"], f"buscar_{info['entidade']}_por_id")
        registro = funcao(id_valor)
        if registro is None:
            return _erro("Registro não encontrado.", 404)
        return jsonify(registro)
    except Exception as e:
        return _erro(str(e), 500)


@app.route("/api/<dominio>/<tabela>", methods=["POST"])
def api_criar(dominio, tabela):
    info = _info_ou_none(dominio, tabela)
    if not info:
        return _erro("Domínio/tabela não encontrado.", 404)
    dados = request.get_json(force=True, silent=True) or {}
    try:
        valores = [dados.get(c) or None for c in info["cols"]]
        funcao = getattr(info["mod"], f"criar_{info['entidade']}")
        novo_id = funcao(*valores)
        return jsonify({"mensagem": "Registro criado com sucesso.", "id": novo_id}), 201
    except Exception as e:
        return _erro(str(e), 500)


@app.route("/api/<dominio>/<tabela>/<id_valor>", methods=["PUT"])
def api_atualizar(dominio, tabela, id_valor):
    info = _info_ou_none(dominio, tabela)
    if not info:
        return _erro("Domínio/tabela não encontrado.", 404)
    dados = request.get_json(force=True, silent=True) or {}
    campos = {c: dados.get(c) for c in info["cols"] if dados.get(c) not in (None, "")}
    if not campos:
        return _erro("Nenhum campo informado para atualizar.")
    try:
        funcao = getattr(info["mod"], f"atualizar_{info['entidade']}")
        linhas = funcao(id_valor, **campos)
        return jsonify({"mensagem": "Registro atualizado com sucesso.", "linhas_afetadas": linhas})
    except Exception as e:
        return _erro(str(e), 500)


@app.route("/api/<dominio>/<tabela>/<id_valor>", methods=["DELETE"])
def api_deletar(dominio, tabela, id_valor):
    info = _info_ou_none(dominio, tabela)
    if not info:
        return _erro("Domínio/tabela não encontrado.", 404)
    try:
        funcao = getattr(info["mod"], f"deletar_{info['entidade']}")
        linhas = funcao(id_valor)
        return jsonify({"mensagem": "Registro excluído com sucesso.", "linhas_afetadas": linhas})
    except Exception as e:
        return _erro(str(e), 500)


# ---------------------------------------------------------------------------
# Consulta SQL livre (somente SELECT) — igual ao op_sql_livre() do main.py.
# ---------------------------------------------------------------------------
@app.route("/api/sql", methods=["POST"])
def api_sql():
    dados = request.get_json(force=True, silent=True) or {}
    query = (dados.get("query") or "").strip()
    if not query.lower().startswith("select"):
        return _erro("Por segurança, esse modo aceita apenas comandos SELECT.")
    try:
        registros = execute_query(query, fetch="all")
        return jsonify({"registros": registros or [], "total": len(registros or [])})
    except Exception as e:
        return _erro(str(e), 500)


# ---------------------------------------------------------------------------
# Ferramentas (Análise e E-mail)
# ---------------------------------------------------------------------------
@app.route("/api/ferramentas/analise", methods=["POST"])
def api_rodar_analise():
    try:
        from main_analise import rodar_pipeline_completo
        rodar_pipeline_completo()
        return jsonify({"mensagem": "Análise rodada com sucesso! Gráficos e CSVs gerados na pasta 'saida'."})
    except Exception as e:
        return _erro(f"Erro ao rodar análise: {str(e)}", 500)

@app.route("/api/ferramentas/email", methods=["POST"])
def api_enviar_email():
    try:
        from analise.email_relatorio import enviar_relatorio_email
        # rodar_pipeline_antes=False: reaproveita os CSVs/gráficos já gerados
        # pelo botão "Gerar Gráficos e CSVs". Rodar a análise completa de novo
        # aqui consome memória demais pro plano gratuito do Render e derruba
        # o worker (SIGKILL / out of memory).
        enviar_relatorio_email(rodar_pipeline_antes=False)
        return jsonify({"mensagem": "Relatório enviado por e-mail com sucesso!"})
    except Exception as e:
        return _erro(f"Erro ao enviar e-mail: {str(e)}", 500)
        
if __name__ == "__main__":
    _porta = int(os.environ.get("PORT", 3000))
    print(f"\n🧳 LuxeVoyage — site rodando em http://localhost:{_porta}  (Ctrl+C para parar)\n")
    app.run(host="0.0.0.0", debug=False, port=_porta)

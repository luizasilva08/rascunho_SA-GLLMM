"""Página inicial — visão geral do banco (métricas + gráfico)."""
import sys
import pathlib

# --- bootstrap de caminho ---------------------------------------------------
# Esta página mora em FRONTEND/paginas/. Como FRONTEND/, SRC/ e TEST/ são
# pastas IRMÃS (nenhuma dentro da outra), o Python não acha `registro`,
# `utils`, `componentes` nem os módulos de domínio (geografia, clientes...)
# sem a gente apontar o caminho de cada uma explicitamente.
_AQUI = pathlib.Path(__file__).resolve()
_FRONTEND = _AQUI.parent.parent      # FRONTEND/
_RAIZ_PROJETO = _FRONTEND.parent      # raiz do projeto
_SRC = _RAIZ_PROJETO / "SRC"          # database.py, utils.py, registro.py
_TEST = _RAIZ_PROJETO / "TEST"        # geografia/, clientes/, analise/, etc.
for _pasta in (_FRONTEND, _SRC, _TEST):
    if str(_pasta) not in sys.path:
        sys.path.insert(0, str(_pasta))
# -----------------------------------------------------------------------------

import streamlit as st
import pandas as pd
from utils import execute_query

st.title("🧳 LuxeVoyage")
st.caption("Painel geral do banco de dados")


def contar(tabela):
    resultado = execute_query(f"SELECT COUNT(*) AS total FROM {tabela}", fetch="one")
    return resultado["total"] if resultado else 0


try:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Clientes", contar("Cliente"))
    col2.metric("Pacotes", contar("Pacote"))
    col3.metric("Parceiros", contar("Parceiros"))
    col4.metric("Viagens", contar("Viagem"))
except Exception as e:
    st.error(f"Não foi possível carregar as métricas: {e}")
    st.info("Confira se o banco está acessível e se o arquivo .env está configurado.")
    st.stop()

st.divider()

st.subheader("Oportunidades por estágio do funil")
try:
    dados = execute_query(
        "SELECT estagio_funil, COUNT(*) AS total FROM Oportunidade_CRM GROUP BY estagio_funil",
        fetch="all",
    )
    if dados:
        df = pd.DataFrame(dados).set_index("estagio_funil")
        st.bar_chart(df)
    else:
        st.info("Nenhuma oportunidade cadastrada ainda.")
except Exception as e:
    st.error(f"Erro ao carregar gráfico: {e}")

st.divider()

st.subheader("Viagens por status")
try:
    dados = execute_query(
        "SELECT status_viagem, COUNT(*) AS total FROM Viagem GROUP BY status_viagem",
        fetch="all",
    )
    if dados:
        df = pd.DataFrame(dados).set_index("status_viagem")
        st.bar_chart(df)
    else:
        st.info("Nenhuma viagem cadastrada ainda.")
except Exception as e:
    st.error(f"Erro ao carregar gráfico: {e}")

st.divider()
st.caption(
    "Use o menu à esquerda para navegar pelos domínios "
    "(Geografia, Parceiros, Catálogo, Clientes, CRM, Comercial, Operacional, Auditoria) "
    "ou para rodar uma consulta SQL livre."
)

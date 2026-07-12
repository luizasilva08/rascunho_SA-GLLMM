"""Página de consulta SQL livre (somente leitura)."""
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

st.title("🛠️ Consulta SQL livre")
st.caption("Por segurança, apenas comandos SELECT são permitidos aqui.")

query = st.text_area(
    "SQL",
    height=140,
    placeholder="SELECT * FROM Cliente LIMIT 10",
)

if st.button("▶️ Executar"):
    if not query.strip().lower().startswith("select"):
        st.error("Por segurança, esse campo só aceita comandos SELECT.")
    else:
        try:
            registros = execute_query(query, fetch="all")
            if registros:
                st.dataframe(pd.DataFrame(registros), use_container_width=True)
                st.caption(f"{len(registros)} registro(s)")
            else:
                st.info("Consulta executada, nenhum resultado retornado.")
        except Exception as e:
            st.error(f"Erro na consulta: {e}")

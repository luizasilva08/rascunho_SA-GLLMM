"""Página do domínio "CRM" — gerada a partir de registro.py."""
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

from registro import REGISTRO
from componentes import render_dominio

render_dominio("CRM", REGISTRO["CRM"])

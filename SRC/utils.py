"""
Funções utilitárias compartilhadas por todos os módulos CRUD.
Centraliza a execução de queries e a montagem de cláusulas SQL dinâmicas.
"""
from database import get_connection


def execute_query(query, params=None, fetch=None, commit=False):
    """
    Executa uma query no banco de dados e gerencia conexão/cursor.

    Parâmetros:
        query   (str)  : comando SQL a ser executado (use %s como placeholder).
        params  (tuple/list): valores para os placeholders da query.
        fetch   (str)  : None | "one" | "all"
                          - "one" retorna um único registro (dict) ou None.
                          - "all" retorna uma lista de registros (dicts).
        commit  (bool) : True para INSERT/UPDATE/DELETE (efetiva a transação).

    Retorno:
        - Se commit=True e for um INSERT: retorna o id gerado (lastrowid),
          ou o número de linhas afetadas quando não há lastrowid (UPDATE/DELETE).
        - Se fetch="one": retorna um dict (ou None).
        - Se fetch="all": retorna uma lista de dicts.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())

        result = None
        if fetch == "one":
            result = cursor.fetchone()
        elif fetch == "all":
            result = cursor.fetchall()

        if commit:
            conn.commit()
            # Para INSERT com AUTO_INCREMENT, lastrowid traz o novo id.
            # Para UPDATE/DELETE, retorna a quantidade de linhas afetadas.
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount

        return result
    finally:
        cursor.close()
        conn.close()


def build_update_clause(campos: dict):
    """
    Monta dinamicamente a cláusula "SET coluna = %s, coluna2 = %s"
    a partir de um dicionário de campos, ignorando valores None.

    Retorna (set_clause: str, params: list).
    Se nenhum campo válido for passado, retorna ("", []).
    """
    set_parts = []
    params = []
    for coluna, valor in campos.items():
        if valor is not None:
            set_parts.append(f"{coluna} = %s")
            params.append(valor)
    return ", ".join(set_parts), params

"""
Módulo CRUD para a tabela Preco_Sazonal.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Preco_Sazonal"
PK = "id_preco"


def criar_preco(id_modulo, id_temporada, valor_sugerido):
    """Insere um novo registro em Preco_Sazonal e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Preco_Sazonal (id_modulo, id_temporada, valor_sugerido)
        VALUES (%s, %s, %s)
    """
    params = (id_modulo, id_temporada, valor_sugerido)
    return execute_query(query, params, commit=True)


def buscar_preco_por_id(id_preco):
    """Retorna um único registro de Preco_Sazonal pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_preco,), fetch="one")


def listar_precos(limit=100, offset=0):
    """Lista registros de Preco_Sazonal com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_precos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Preco_Sazonal filtrando por um único campo/coluna.
    Ex: buscar_precos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_preco(id_preco, **campos):
    """
    Atualiza os campos informados de um registro de Preco_Sazonal.
    Ex: atualizar_preco(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_preco)
    return execute_query(query, params, commit=True)


def deletar_preco(id_preco):
    """Remove um registro de Preco_Sazonal pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_preco,), commit=True)

"""
Módulo CRUD para a tabela Parceiros.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Parceiros"
PK = "id_parceiro"


def criar_parceiro(razao_social, tipo_parceiro, status):
    """Insere um novo registro em Parceiros e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Parceiros (razao_social, tipo_parceiro, status)
        VALUES (%s, %s, %s)
    """
    params = (razao_social, tipo_parceiro, status)
    return execute_query(query, params, commit=True)


def buscar_parceiro_por_id(id_parceiro):
    """Retorna um único registro de Parceiros pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_parceiro,), fetch="one")


def listar_parceiros(limit=100, offset=0):
    """Lista registros de Parceiros com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_parceiros_por_campo(campo, valor, limit=100):
    """
    Busca registros de Parceiros filtrando por um único campo/coluna.
    Ex: buscar_parceiros_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_parceiro(id_parceiro, **campos):
    """
    Atualiza os campos informados de um registro de Parceiros.
    Ex: atualizar_parceiro(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_parceiro)
    return execute_query(query, params, commit=True)


def deletar_parceiro(id_parceiro):
    """Remove um registro de Parceiros pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_parceiro,), commit=True)

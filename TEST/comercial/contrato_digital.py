"""
Módulo CRUD para a tabela Contrato_Digital.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Contrato_Digital"
PK = "id_contrato"


def criar_contrato(id_proposta, timestamp_aceite, ip_aceite, hash_integridade, status):
    """Insere um novo registro em Contrato_Digital e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Contrato_Digital (id_proposta, timestamp_aceite, ip_aceite, hash_integridade, status)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (id_proposta, timestamp_aceite, ip_aceite, hash_integridade, status)
    return execute_query(query, params, commit=True)


def buscar_contrato_por_id(id_contrato):
    """Retorna um único registro de Contrato_Digital pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_contrato,), fetch="one")


def listar_contratos(limit=100, offset=0):
    """Lista registros de Contrato_Digital com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_contratos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Contrato_Digital filtrando por um único campo/coluna.
    Ex: buscar_contratos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_contrato(id_contrato, **campos):
    """
    Atualiza os campos informados de um registro de Contrato_Digital.
    Ex: atualizar_contrato(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_contrato)
    return execute_query(query, params, commit=True)


def deletar_contrato(id_contrato):
    """Remove um registro de Contrato_Digital pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_contrato,), commit=True)

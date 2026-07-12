"""
Módulo CRUD para a tabela Consentimentos_LGPD.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Consentimentos_LGPD"
PK = "id_consentimento"


def criar_consentimento(id_cliente, tipo_consentimento, status):
    """Insere um novo registro em Consentimentos_LGPD e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Consentimentos_LGPD (id_cliente, tipo_consentimento, status)
        VALUES (%s, %s, %s)
    """
    params = (id_cliente, tipo_consentimento, status)
    return execute_query(query, params, commit=True)


def buscar_consentimento_por_id(id_consentimento):
    """Retorna um único registro de Consentimentos_LGPD pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_consentimento,), fetch="one")


def listar_consentimentos(limit=100, offset=0):
    """Lista registros de Consentimentos_LGPD com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_consentimentos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Consentimentos_LGPD filtrando por um único campo/coluna.
    Ex: buscar_consentimentos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_consentimento(id_consentimento, **campos):
    """
    Atualiza os campos informados de um registro de Consentimentos_LGPD.
    Ex: atualizar_consentimento(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_consentimento)
    return execute_query(query, params, commit=True)


def deletar_consentimento(id_consentimento):
    """Remove um registro de Consentimentos_LGPD pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_consentimento,), commit=True)

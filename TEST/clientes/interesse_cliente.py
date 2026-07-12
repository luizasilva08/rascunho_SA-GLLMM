"""
Módulo CRUD para a tabela Interesses_Cliente.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Interesses_Cliente"
PK = "id_interesse"


def criar_interesse(id_cliente, id_municipio_destino, status):
    """Insere um novo registro em Interesses_Cliente e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Interesses_Cliente (id_cliente, id_municipio_destino, status)
        VALUES (%s, %s, %s)
    """
    params = (id_cliente, id_municipio_destino, status)
    return execute_query(query, params, commit=True)


def buscar_interesse_por_id(id_interesse):
    """Retorna um único registro de Interesses_Cliente pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_interesse,), fetch="one")


def listar_interesses(limit=100, offset=0):
    """Lista registros de Interesses_Cliente com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_interesses_por_campo(campo, valor, limit=100):
    """
    Busca registros de Interesses_Cliente filtrando por um único campo/coluna.
    Ex: buscar_interesses_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_interesse(id_interesse, **campos):
    """
    Atualiza os campos informados de um registro de Interesses_Cliente.
    Ex: atualizar_interesse(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_interesse)
    return execute_query(query, params, commit=True)


def deletar_interesse(id_interesse):
    """Remove um registro de Interesses_Cliente pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_interesse,), commit=True)

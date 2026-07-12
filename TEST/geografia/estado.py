"""
Módulo CRUD para a tabela Estado.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Estado"
PK = "id_estado"


def criar_estado(sigla, nome, regiao_nome, timezone):
    """Insere um novo registro em Estado e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Estado (sigla, nome, regiao_nome, timezone)
        VALUES (%s, %s, %s, %s)
    """
    params = (sigla, nome, regiao_nome, timezone)
    return execute_query(query, params, commit=True)


def buscar_estado_por_id(id_estado):
    """Retorna um único registro de Estado pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_estado,), fetch="one")


def listar_estados(limit=100, offset=0):
    """Lista registros de Estado com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_estados_por_campo(campo, valor, limit=100):
    """
    Busca registros de Estado filtrando por um único campo/coluna.
    Ex: buscar_estados_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_estado(id_estado, **campos):
    """
    Atualiza os campos informados de um registro de Estado.
    Ex: atualizar_estado(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_estado)
    return execute_query(query, params, commit=True)


def deletar_estado(id_estado):
    """Remove um registro de Estado pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_estado,), commit=True)

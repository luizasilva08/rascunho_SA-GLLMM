"""
Módulo CRUD para a tabela Municipio.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Municipio"
PK = "id_municipio"


def criar_municipio(id_estado, nome, categoria):
    """Insere um novo registro em Municipio e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Municipio (id_estado, nome, categoria)
        VALUES (%s, %s, %s)
    """
    params = (id_estado, nome, categoria)
    return execute_query(query, params, commit=True)


def buscar_municipio_por_id(id_municipio):
    """Retorna um único registro de Municipio pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_municipio,), fetch="one")


def listar_municipios(limit=100, offset=0):
    """Lista registros de Municipio com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_municipios_por_campo(campo, valor, limit=100):
    """
    Busca registros de Municipio filtrando por um único campo/coluna.
    Ex: buscar_municipios_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_municipio(id_municipio, **campos):
    """
    Atualiza os campos informados de um registro de Municipio.
    Ex: atualizar_municipio(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_municipio)
    return execute_query(query, params, commit=True)


def deletar_municipio(id_municipio):
    """Remove um registro de Municipio pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_municipio,), commit=True)

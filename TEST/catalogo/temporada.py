"""
Módulo CRUD para a tabela Temporada.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Temporada"
PK = "id_temporada"


def criar_temporada(nome, data_inicio, data_fim):
    """Insere um novo registro em Temporada e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Temporada (nome, data_inicio, data_fim)
        VALUES (%s, %s, %s)
    """
    params = (nome, data_inicio, data_fim)
    return execute_query(query, params, commit=True)


def buscar_temporada_por_id(id_temporada):
    """Retorna um único registro de Temporada pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_temporada,), fetch="one")


def listar_temporadas(limit=100, offset=0):
    """Lista registros de Temporada com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_temporadas_por_campo(campo, valor, limit=100):
    """
    Busca registros de Temporada filtrando por um único campo/coluna.
    Ex: buscar_temporadas_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_temporada(id_temporada, **campos):
    """
    Atualiza os campos informados de um registro de Temporada.
    Ex: atualizar_temporada(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_temporada)
    return execute_query(query, params, commit=True)


def deletar_temporada(id_temporada):
    """Remove um registro de Temporada pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_temporada,), commit=True)

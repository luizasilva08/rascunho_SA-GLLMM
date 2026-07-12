"""
Módulo CRUD para a tabela Destaques_Sazonais.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Destaques_Sazonais"
PK = "id_destaque"


def criar_destaque(id_municipio, data_inicio, data_fim, classificacao):
    """Insere um novo registro em Destaques_Sazonais e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Destaques_Sazonais (id_municipio, data_inicio, data_fim, classificacao)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_municipio, data_inicio, data_fim, classificacao)
    return execute_query(query, params, commit=True)


def buscar_destaque_por_id(id_destaque):
    """Retorna um único registro de Destaques_Sazonais pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_destaque,), fetch="one")


def listar_destaques(limit=100, offset=0):
    """Lista registros de Destaques_Sazonais com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_destaques_por_campo(campo, valor, limit=100):
    """
    Busca registros de Destaques_Sazonais filtrando por um único campo/coluna.
    Ex: buscar_destaques_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_destaque(id_destaque, **campos):
    """
    Atualiza os campos informados de um registro de Destaques_Sazonais.
    Ex: atualizar_destaque(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_destaque)
    return execute_query(query, params, commit=True)


def deletar_destaque(id_destaque):
    """Remove um registro de Destaques_Sazonais pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_destaque,), commit=True)

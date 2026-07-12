"""
Módulo CRUD para a tabela Solicitacao_SLA.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Solicitacao_SLA"
PK = "id_solicitacao"


def criar_solicitacao(id_oportunidade, id_parceiro, data_envio, status):
    """Insere um novo registro em Solicitacao_SLA e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Solicitacao_SLA (id_oportunidade, id_parceiro, data_envio, status)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_oportunidade, id_parceiro, data_envio, status)
    return execute_query(query, params, commit=True)


def buscar_solicitacao_por_id(id_solicitacao):
    """Retorna um único registro de Solicitacao_SLA pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_solicitacao,), fetch="one")


def listar_solicitacoes(limit=100, offset=0):
    """Lista registros de Solicitacao_SLA com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_solicitacoes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Solicitacao_SLA filtrando por um único campo/coluna.
    Ex: buscar_solicitacoes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_solicitacao(id_solicitacao, **campos):
    """
    Atualiza os campos informados de um registro de Solicitacao_SLA.
    Ex: atualizar_solicitacao(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_solicitacao)
    return execute_query(query, params, commit=True)


def deletar_solicitacao(id_solicitacao):
    """Remove um registro de Solicitacao_SLA pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_solicitacao,), commit=True)

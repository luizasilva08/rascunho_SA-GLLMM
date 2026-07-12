"""
Módulo CRUD para a tabela Propostas_Comerciais.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Propostas_Comerciais"
PK = "id_proposta"


def criar_proposta(id_cotacao, versao, status):
    """Insere um novo registro em Propostas_Comerciais e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Propostas_Comerciais (id_cotacao, versao, status)
        VALUES (%s, %s, %s)
    """
    params = (id_cotacao, versao, status)
    return execute_query(query, params, commit=True)


def buscar_proposta_por_id(id_proposta):
    """Retorna um único registro de Propostas_Comerciais pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_proposta,), fetch="one")


def listar_propostas(limit=100, offset=0):
    """Lista registros de Propostas_Comerciais com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_propostas_por_campo(campo, valor, limit=100):
    """
    Busca registros de Propostas_Comerciais filtrando por um único campo/coluna.
    Ex: buscar_propostas_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_proposta(id_proposta, **campos):
    """
    Atualiza os campos informados de um registro de Propostas_Comerciais.
    Ex: atualizar_proposta(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_proposta)
    return execute_query(query, params, commit=True)


def deletar_proposta(id_proposta):
    """Remove um registro de Propostas_Comerciais pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_proposta,), commit=True)

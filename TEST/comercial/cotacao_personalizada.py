"""
Módulo CRUD para a tabela Cotacao_Personalizadas.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Cotacao_Personalizadas"
PK = "id_cotacao"


def criar_cotacao(id_oportunidade, id_pacote, valor_total_calculado, status):
    """Insere um novo registro em Cotacao_Personalizadas e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Cotacao_Personalizadas (id_oportunidade, id_pacote, valor_total_calculado, status)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_oportunidade, id_pacote, valor_total_calculado, status)
    return execute_query(query, params, commit=True)


def buscar_cotacao_por_id(id_cotacao):
    """Retorna um único registro de Cotacao_Personalizadas pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cotacao,), fetch="one")


def listar_cotacoes(limit=100, offset=0):
    """Lista registros de Cotacao_Personalizadas com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_cotacoes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Cotacao_Personalizadas filtrando por um único campo/coluna.
    Ex: buscar_cotacoes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_cotacao(id_cotacao, **campos):
    """
    Atualiza os campos informados de um registro de Cotacao_Personalizadas.
    Ex: atualizar_cotacao(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_cotacao)
    return execute_query(query, params, commit=True)


def deletar_cotacao(id_cotacao):
    """Remove um registro de Cotacao_Personalizadas pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cotacao,), commit=True)

"""
Módulo CRUD para a tabela Item_Cotacao.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Item_Cotacao"
PK = "id_item_cotacao"


def criar_item(id_cotacao, id_modulo, valor_aplicado):
    """Insere um novo registro em Item_Cotacao e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Item_Cotacao (id_cotacao, id_modulo, valor_aplicado)
        VALUES (%s, %s, %s)
    """
    params = (id_cotacao, id_modulo, valor_aplicado)
    return execute_query(query, params, commit=True)


def buscar_item_por_id(id_item_cotacao):
    """Retorna um único registro de Item_Cotacao pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_item_cotacao,), fetch="one")


def listar_itens(limit=100, offset=0):
    """Lista registros de Item_Cotacao com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_itens_por_campo(campo, valor, limit=100):
    """
    Busca registros de Item_Cotacao filtrando por um único campo/coluna.
    Ex: buscar_itens_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_item(id_item_cotacao, **campos):
    """
    Atualiza os campos informados de um registro de Item_Cotacao.
    Ex: atualizar_item(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_item_cotacao)
    return execute_query(query, params, commit=True)


def deletar_item(id_item_cotacao):
    """Remove um registro de Item_Cotacao pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_item_cotacao,), commit=True)

"""
Módulo CRUD para a tabela Pagamento_Contrato.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Pagamento_Contrato"
PK = "id_pagamento"


def criar_pagamento(id_contrato, metodo_pagamento, valor_total, numero_parcela, total_parcelas, status_transacao):
    """Insere um novo registro em Pagamento_Contrato e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Pagamento_Contrato (id_contrato, metodo_pagamento, valor_total, numero_parcela, total_parcelas, status_transacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (id_contrato, metodo_pagamento, valor_total, numero_parcela, total_parcelas, status_transacao)
    return execute_query(query, params, commit=True)


def buscar_pagamento_por_id(id_pagamento):
    """Retorna um único registro de Pagamento_Contrato pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_pagamento,), fetch="one")


def listar_pagamentos(limit=100, offset=0):
    """Lista registros de Pagamento_Contrato com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_pagamentos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Pagamento_Contrato filtrando por um único campo/coluna.
    Ex: buscar_pagamentos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_pagamento(id_pagamento, **campos):
    """
    Atualiza os campos informados de um registro de Pagamento_Contrato.
    Ex: atualizar_pagamento(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_pagamento)
    return execute_query(query, params, commit=True)


def deletar_pagamento(id_pagamento):
    """Remove um registro de Pagamento_Contrato pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_pagamento,), commit=True)

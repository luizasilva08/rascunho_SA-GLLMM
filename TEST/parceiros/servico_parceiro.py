"""
Módulo CRUD para a tabela Servicos_Parceiros.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Servicos_Parceiros"
PK = "id_servico_parceiro"


def criar_servico(id_parceiro, categoria_servico, nome_servico):
    """Insere um novo registro em Servicos_Parceiros e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Servicos_Parceiros (id_parceiro, categoria_servico, nome_servico)
        VALUES (%s, %s, %s)
    """
    params = (id_parceiro, categoria_servico, nome_servico)
    return execute_query(query, params, commit=True)


def buscar_servico_por_id(id_servico_parceiro):
    """Retorna um único registro de Servicos_Parceiros pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_servico_parceiro,), fetch="one")


def listar_servicos(limit=100, offset=0):
    """Lista registros de Servicos_Parceiros com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_servicos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Servicos_Parceiros filtrando por um único campo/coluna.
    Ex: buscar_servicos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_servico(id_servico_parceiro, **campos):
    """
    Atualiza os campos informados de um registro de Servicos_Parceiros.
    Ex: atualizar_servico(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_servico_parceiro)
    return execute_query(query, params, commit=True)


def deletar_servico(id_servico_parceiro):
    """Remove um registro de Servicos_Parceiros pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_servico_parceiro,), commit=True)

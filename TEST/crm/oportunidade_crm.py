"""
Módulo CRUD para a tabela Oportunidade_CRM.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Oportunidade_CRM"
PK = "id_oportunidade"


def criar_oportunidade(id_cliente, id_usuario_interno, estagio_funil, valor_estimado):
    """Insere um novo registro em Oportunidade_CRM e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Oportunidade_CRM (id_cliente, id_usuario_interno, estagio_funil, valor_estimado)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_cliente, id_usuario_interno, estagio_funil, valor_estimado)
    return execute_query(query, params, commit=True)


def buscar_oportunidade_por_id(id_oportunidade):
    """Retorna um único registro de Oportunidade_CRM pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_oportunidade,), fetch="one")


def listar_oportunidades(limit=100, offset=0):
    """Lista registros de Oportunidade_CRM com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_oportunidades_por_campo(campo, valor, limit=100):
    """
    Busca registros de Oportunidade_CRM filtrando por um único campo/coluna.
    Ex: buscar_oportunidades_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_oportunidade(id_oportunidade, **campos):
    """
    Atualiza os campos informados de um registro de Oportunidade_CRM.
    Ex: atualizar_oportunidade(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_oportunidade)
    return execute_query(query, params, commit=True)


def deletar_oportunidade(id_oportunidade):
    """Remove um registro de Oportunidade_CRM pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_oportunidade,), commit=True)

"""
Módulo CRUD para a tabela Historico_Interacoes.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Historico_Interacoes"
PK = "id_interacao"


def criar_interacao(id_oportunidade, id_cliente, id_usuario_interno, tipo_interacao, data_interacao):
    """Insere um novo registro em Historico_Interacoes e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Historico_Interacoes (id_oportunidade, id_cliente, id_usuario_interno, tipo_interacao, data_interacao)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (id_oportunidade, id_cliente, id_usuario_interno, tipo_interacao, data_interacao)
    return execute_query(query, params, commit=True)


def buscar_interacao_por_id(id_interacao):
    """Retorna um único registro de Historico_Interacoes pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_interacao,), fetch="one")


def listar_interacoes(limit=100, offset=0):
    """Lista registros de Historico_Interacoes com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_interacoes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Historico_Interacoes filtrando por um único campo/coluna.
    Ex: buscar_interacoes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_interacao(id_interacao, **campos):
    """
    Atualiza os campos informados de um registro de Historico_Interacoes.
    Ex: atualizar_interacao(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_interacao)
    return execute_query(query, params, commit=True)


def deletar_interacao(id_interacao):
    """Remove um registro de Historico_Interacoes pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_interacao,), commit=True)

"""
Módulo CRUD para a tabela Avaliacoes_Parceiros.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Avaliacoes_Parceiros"
PK = "id_avaliacao"


def criar_avaliacao(id_parceiro, id_usuario_interno, nota, comentarios):
    """Insere um novo registro em Avaliacoes_Parceiros e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Avaliacoes_Parceiros (id_parceiro, id_usuario_interno, nota, comentarios)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_parceiro, id_usuario_interno, nota, comentarios)
    return execute_query(query, params, commit=True)


def buscar_avaliacao_por_id(id_avaliacao):
    """Retorna um único registro de Avaliacoes_Parceiros pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_avaliacao,), fetch="one")


def listar_avaliacoes(limit=100, offset=0):
    """Lista registros de Avaliacoes_Parceiros com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_avaliacoes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Avaliacoes_Parceiros filtrando por um único campo/coluna.
    Ex: buscar_avaliacoes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_avaliacao(id_avaliacao, **campos):
    """
    Atualiza os campos informados de um registro de Avaliacoes_Parceiros.
    Ex: atualizar_avaliacao(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_avaliacao)
    return execute_query(query, params, commit=True)


def deletar_avaliacao(id_avaliacao):
    """Remove um registro de Avaliacoes_Parceiros pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_avaliacao,), commit=True)

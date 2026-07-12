"""
Módulo CRUD para a tabela Pacote.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Pacote"
PK = "id_pacote"


def criar_pacote(nome_pacote, id_municipio_destino, status):
    """Insere um novo registro em Pacote e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Pacote (nome_pacote, id_municipio_destino, status)
        VALUES (%s, %s, %s)
    """
    params = (nome_pacote, id_municipio_destino, status)
    return execute_query(query, params, commit=True)


def buscar_pacote_por_id(id_pacote):
    """Retorna um único registro de Pacote pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_pacote,), fetch="one")


def listar_pacotes(limit=100, offset=0):
    """Lista registros de Pacote com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_pacotes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Pacote filtrando por um único campo/coluna.
    Ex: buscar_pacotes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_pacote(id_pacote, **campos):
    """
    Atualiza os campos informados de um registro de Pacote.
    Ex: atualizar_pacote(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_pacote)
    return execute_query(query, params, commit=True)


def deletar_pacote(id_pacote):
    """Remove um registro de Pacote pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_pacote,), commit=True)

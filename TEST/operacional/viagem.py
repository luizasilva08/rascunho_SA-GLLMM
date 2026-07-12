"""
Módulo CRUD para a tabela Viagem.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Viagem"
PK = "id_viagem"


def criar_viagem(id_contrato, data_embarque, data_retorno, status_viagem):
    """Insere um novo registro em Viagem e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Viagem (id_contrato, data_embarque, data_retorno, status_viagem)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_contrato, data_embarque, data_retorno, status_viagem)
    return execute_query(query, params, commit=True)


def buscar_viagem_por_id(id_viagem):
    """Retorna um único registro de Viagem pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_viagem,), fetch="one")


def listar_viagens(limit=100, offset=0):
    """Lista registros de Viagem com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_viagens_por_campo(campo, valor, limit=100):
    """
    Busca registros de Viagem filtrando por um único campo/coluna.
    Ex: buscar_viagens_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_viagem(id_viagem, **campos):
    """
    Atualiza os campos informados de um registro de Viagem.
    Ex: atualizar_viagem(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_viagem)
    return execute_query(query, params, commit=True)


def deletar_viagem(id_viagem):
    """Remove um registro de Viagem pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_viagem,), commit=True)

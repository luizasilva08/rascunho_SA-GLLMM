"""
Módulo CRUD para a tabela Cobertura_Parceiros.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Cobertura_Parceiros"
PK = "id_cobertura"


def criar_cobertura(id_parceiro, id_municipio, status):
    """Insere um novo registro em Cobertura_Parceiros e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Cobertura_Parceiros (id_parceiro, id_municipio, status)
        VALUES (%s, %s, %s)
    """
    params = (id_parceiro, id_municipio, status)
    return execute_query(query, params, commit=True)


def buscar_cobertura_por_id(id_cobertura):
    """Retorna um único registro de Cobertura_Parceiros pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cobertura,), fetch="one")


def listar_coberturas(limit=100, offset=0):
    """Lista registros de Cobertura_Parceiros com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_coberturas_por_campo(campo, valor, limit=100):
    """
    Busca registros de Cobertura_Parceiros filtrando por um único campo/coluna.
    Ex: buscar_coberturas_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_cobertura(id_cobertura, **campos):
    """
    Atualiza os campos informados de um registro de Cobertura_Parceiros.
    Ex: atualizar_cobertura(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_cobertura)
    return execute_query(query, params, commit=True)


def deletar_cobertura(id_cobertura):
    """Remove um registro de Cobertura_Parceiros pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cobertura,), commit=True)

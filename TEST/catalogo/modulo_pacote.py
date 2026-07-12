"""
Módulo CRUD para a tabela Modulos_Pacote.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Modulos_Pacote"
PK = "id_modulo"


def criar_modulo(id_pacote, id_servico_parceiro, obrigatorio):
    """Insere um novo registro em Modulos_Pacote e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Modulos_Pacote (id_pacote, id_servico_parceiro, obrigatorio)
        VALUES (%s, %s, %s)
    """
    params = (id_pacote, id_servico_parceiro, obrigatorio)
    return execute_query(query, params, commit=True)


def buscar_modulo_por_id(id_modulo):
    """Retorna um único registro de Modulos_Pacote pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_modulo,), fetch="one")


def listar_modulos(limit=100, offset=0):
    """Lista registros de Modulos_Pacote com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_modulos_por_campo(campo, valor, limit=100):
    """
    Busca registros de Modulos_Pacote filtrando por um único campo/coluna.
    Ex: buscar_modulos_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_modulo(id_modulo, **campos):
    """
    Atualiza os campos informados de um registro de Modulos_Pacote.
    Ex: atualizar_modulo(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_modulo)
    return execute_query(query, params, commit=True)


def deletar_modulo(id_modulo):
    """Remove um registro de Modulos_Pacote pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_modulo,), commit=True)

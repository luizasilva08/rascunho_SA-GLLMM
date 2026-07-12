"""
Módulo CRUD para a tabela Log_Acesso.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Log_Acesso"
PK = "id_log"


def criar_log(id_usuario_interno, id_cliente, tipo_operacao, data_acesso):
    """Insere um novo registro em Log_Acesso e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Log_Acesso (id_usuario_interno, id_cliente, tipo_operacao, data_acesso)
        VALUES (%s, %s, %s, %s)
    """
    params = (id_usuario_interno, id_cliente, tipo_operacao, data_acesso)
    return execute_query(query, params, commit=True)


def buscar_log_por_id(id_log):
    """Retorna um único registro de Log_Acesso pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_log,), fetch="one")


def listar_logs(limit=100, offset=0):
    """Lista registros de Log_Acesso com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_logs_por_campo(campo, valor, limit=100):
    """
    Busca registros de Log_Acesso filtrando por um único campo/coluna.
    Ex: buscar_logs_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_log(id_log, **campos):
    """
    Atualiza os campos informados de um registro de Log_Acesso.
    Ex: atualizar_log(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_log)
    return execute_query(query, params, commit=True)


def deletar_log(id_log):
    """Remove um registro de Log_Acesso pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_log,), commit=True)

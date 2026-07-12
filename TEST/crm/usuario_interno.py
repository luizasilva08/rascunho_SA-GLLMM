"""
Módulo CRUD para a tabela Usuario_Interno.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Usuario_Interno"
PK = "id_usuario_interno"


def criar_usuario(nome, cargo, email_corporativo, nivel_acesso):
    """Insere um novo registro em Usuario_Interno e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Usuario_Interno (nome, cargo, email_corporativo, nivel_acesso)
        VALUES (%s, %s, %s, %s)
    """
    params = (nome, cargo, email_corporativo, nivel_acesso)
    return execute_query(query, params, commit=True)


def buscar_usuario_por_id(id_usuario_interno):
    """Retorna um único registro de Usuario_Interno pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_usuario_interno,), fetch="one")


def listar_usuarios(limit=100, offset=0):
    """Lista registros de Usuario_Interno com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_usuarios_por_campo(campo, valor, limit=100):
    """
    Busca registros de Usuario_Interno filtrando por um único campo/coluna.
    Ex: buscar_usuarios_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_usuario(id_usuario_interno, **campos):
    """
    Atualiza os campos informados de um registro de Usuario_Interno.
    Ex: atualizar_usuario(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_usuario_interno)
    return execute_query(query, params, commit=True)


def deletar_usuario(id_usuario_interno):
    """Remove um registro de Usuario_Interno pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_usuario_interno,), commit=True)

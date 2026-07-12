"""
Módulo CRUD para a tabela Cliente.
Gerado para o banco de dados LuxeVoyage.
"""
from utils import execute_query, build_update_clause

TABLE = "Cliente"
PK = "id_cliente"


def criar_cliente(nome, cpf_criptografado, email_criptografado, telefone_criptografado, cep, id_municipio_origem):
    """Insere um novo registro em Cliente e retorna o id gerado (lastrowid)."""
    query = """
        INSERT INTO Cliente (nome, cpf_criptografado, email_criptografado, telefone_criptografado, cep, id_municipio_origem)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (nome, cpf_criptografado, email_criptografado, telefone_criptografado, cep, id_municipio_origem)
    return execute_query(query, params, commit=True)


def buscar_cliente_por_id(id_cliente):
    """Retorna um único registro de Cliente pelo id, ou None se não existir."""
    query = f"SELECT * FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cliente,), fetch="one")


def listar_clientes(limit=100, offset=0):
    """Lista registros de Cliente com paginação simples."""
    query = f"SELECT * FROM {TABLE} ORDER BY {PK} LIMIT %s OFFSET %s"
    return execute_query(query, (limit, offset), fetch="all")


def buscar_clientes_por_campo(campo, valor, limit=100):
    """
    Busca registros de Cliente filtrando por um único campo/coluna.
    Ex: buscar_clientes_por_campo("status", "Ativo")
    """
    query = f"SELECT * FROM {TABLE} WHERE {campo} = %s LIMIT %s"
    return execute_query(query, (valor, limit), fetch="all")


def atualizar_cliente(id_cliente, **campos):
    """
    Atualiza os campos informados de um registro de Cliente.
    Ex: atualizar_cliente(1, status="Inativo")
    """
    set_clause, params = build_update_clause(campos)
    if not set_clause:
        return 0
    query = f"UPDATE {TABLE} SET {set_clause} WHERE {PK} = %s"
    params.append(id_cliente)
    return execute_query(query, params, commit=True)


def deletar_cliente(id_cliente):
    """Remove um registro de Cliente pelo id."""
    query = f"DELETE FROM {TABLE} WHERE {PK} = %s"
    return execute_query(query, (id_cliente,), commit=True)

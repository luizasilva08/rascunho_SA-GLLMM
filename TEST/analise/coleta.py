"""
analise/coleta.py — extração de dados do banco LuxeVoyage para pandas.

Cada função roda uma consulta (via utils.execute_query, o mesmo usado pelo
CRUD) e devolve um DataFrame "cru" — sem tratamento ainda. O tratamento
(tipos, nulos, nomes de coluna) fica todo em analise/tratamento.py, de
propósito: separar "buscar dado" de "arrumar dado" deixa cada função fácil
de testar e reaproveitar sozinha.
"""
import pandas as pd
from utils import execute_query


def extrair_clientes() -> pd.DataFrame:
    """Clientes, já com o nome do município/estado de origem."""
    query = """
        SELECT
            c.id_cliente, c.nome, c.cep,
            m.nome AS municipio_origem,
            e.nome AS estado_origem,
            e.sigla AS uf_origem
        FROM Cliente c
        LEFT JOIN Municipio m ON m.id_municipio = c.id_municipio_origem
        LEFT JOIN Estado e ON e.id_estado = m.id_estado
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_pacotes() -> pd.DataFrame:
    """Pacotes turísticos, com o nome do destino."""
    query = """
        SELECT
            p.id_pacote, p.nome_pacote, p.status,
            m.nome AS destino, e.sigla AS uf_destino
        FROM Pacote p
        JOIN Municipio m ON m.id_municipio = p.id_municipio_destino
        JOIN Estado e ON e.id_estado = m.id_estado
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_oportunidades() -> pd.DataFrame:
    """Oportunidades do funil de vendas (CRM)."""
    query = """
        SELECT id_oportunidade, id_cliente, id_usuario_interno,
               estagio_funil, valor_estimado
        FROM Oportunidade_CRM
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_contratos() -> pd.DataFrame:
    """Contratos assinados, com a data de aceite."""
    query = """
        SELECT id_contrato, id_proposta, timestamp_aceite, status
        FROM Contrato_Digital
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_pagamentos() -> pd.DataFrame:
    """Pagamentos, já com a data do contrato (pra análises por mês)."""
    query = """
        SELECT
            pg.id_pagamento, pg.id_contrato, pg.metodo_pagamento,
            pg.valor_total, pg.status_transacao,
            cd.timestamp_aceite
        FROM Pagamento_Contrato pg
        JOIN Contrato_Digital cd ON cd.id_contrato = pg.id_contrato
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_avaliacoes() -> pd.DataFrame:
    """Avaliações internas dos parceiros."""
    query = """
        SELECT
            a.id_avaliacao, a.nota, a.comentarios,
            p.id_parceiro, p.razao_social, p.tipo_parceiro
        FROM Avaliacoes_Parceiros a
        JOIN Parceiros p ON p.id_parceiro = a.id_parceiro
    """
    return pd.DataFrame(execute_query(query, fetch="all"))


def extrair_viagens() -> pd.DataFrame:
    """Viagens confirmadas/realizadas, com o nome do pacote."""
    query = """
        SELECT
            v.id_viagem, v.data_embarque, v.data_retorno, v.status_viagem,
            p.nome_pacote
        FROM Viagem v
        JOIN Contrato_Digital cd ON cd.id_contrato = v.id_contrato
        JOIN Propostas_Comerciais pr ON pr.id_proposta = cd.id_proposta
        JOIN Cotacao_Personalizadas cot ON cot.id_cotacao = pr.id_cotacao
        JOIN Pacote p ON p.id_pacote = cot.id_pacote
    """
    return pd.DataFrame(execute_query(query, fetch="all"))

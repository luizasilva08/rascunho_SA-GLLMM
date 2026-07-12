"""
analise/tratamento.py — limpeza e padronização dos dados (equivalente ao
"corrigir os cabeçalhos" / groupby do notebook original, só que mais
completo: tipos, nulos e texto também são tratados aqui).

Cada função recebe o DataFrame "cru" (vindo de analise/coleta.py) e
devolve uma cópia tratada — nunca modifica o original.
"""
import pandas as pd


def _padronizar_texto(serie: pd.Series) -> pd.Series:
    """Remove espaços nas pontas e uniformiza capitalização de campos de texto."""
    return serie.astype(str).str.strip().replace({"None": pd.NA, "": pd.NA})


def tratar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["municipio_origem"] = _padronizar_texto(df["municipio_origem"]).fillna("Não informado")
    df["uf_origem"] = _padronizar_texto(df["uf_origem"]).fillna("N/D")
    df["cep"] = df["cep"].fillna("Não informado")
    return df


def tratar_pacotes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["status"] = _padronizar_texto(df["status"]).fillna("Sem status")
    df["destino"] = _padronizar_texto(df["destino"])
    return df


def tratar_oportunidades(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["estagio_funil"] = _padronizar_texto(df["estagio_funil"]).fillna("Sem estágio")
    # valor_estimado às vezes vem como Decimal (do MySQL) — converte pra float
    df["valor_estimado"] = pd.to_numeric(df["valor_estimado"], errors="coerce").fillna(0.0)
    return df


def tratar_contratos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["timestamp_aceite"] = pd.to_datetime(df["timestamp_aceite"], errors="coerce")
    df["status"] = _padronizar_texto(df["status"]).fillna("Sem status")
    return df


def tratar_pagamentos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["valor_total"] = pd.to_numeric(df["valor_total"], errors="coerce").fillna(0.0)
    df["timestamp_aceite"] = pd.to_datetime(df["timestamp_aceite"], errors="coerce")
    df["mes_referencia"] = df["timestamp_aceite"].dt.to_period("M").astype(str)
    df["status_transacao"] = _padronizar_texto(df["status_transacao"]).fillna("Pendente")
    return df


def tratar_avaliacoes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["nota"] = pd.to_numeric(df["nota"], errors="coerce")
    df = df.dropna(subset=["nota"])
    df["razao_social"] = _padronizar_texto(df["razao_social"])
    return df


def tratar_viagens(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df
    df["data_embarque"] = pd.to_datetime(df["data_embarque"], errors="coerce")
    df["data_retorno"] = pd.to_datetime(df["data_retorno"], errors="coerce")
    df["status_viagem"] = _padronizar_texto(df["status_viagem"]).fillna("Sem status")
    df["mes_embarque"] = df["data_embarque"].dt.to_period("M").astype(str)
    return df

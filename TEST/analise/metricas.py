"""
analise/metricas.py — as análises em si (equivalente ao dataset.groupby()
do notebook original). Cada função recebe um DataFrame já tratado e
devolve uma Series/DataFrame resumido, pronto pra virar gráfico ou tabela.
"""
import pandas as pd


def clientes_por_estado(df_clientes: pd.DataFrame) -> pd.Series:
    if df_clientes.empty:
        return pd.Series(dtype="int64")
    return df_clientes.groupby("uf_origem").size().sort_values(ascending=False)


def pacotes_por_status(df_pacotes: pd.DataFrame) -> pd.Series:
    if df_pacotes.empty:
        return pd.Series(dtype="int64")
    return df_pacotes.groupby("status").size().sort_values(ascending=False)


def pacotes_por_destino(df_pacotes: pd.DataFrame, top_n: int = 10) -> pd.Series:
    if df_pacotes.empty:
        return pd.Series(dtype="int64")
    return df_pacotes.groupby("destino").size().sort_values(ascending=False).head(top_n)


def oportunidades_por_estagio(df_oportunidades: pd.DataFrame) -> pd.Series:
    if df_oportunidades.empty:
        return pd.Series(dtype="int64")
    return df_oportunidades.groupby("estagio_funil").size().sort_values(ascending=False)


def valor_estimado_por_estagio(df_oportunidades: pd.DataFrame) -> pd.Series:
    if df_oportunidades.empty:
        return pd.Series(dtype="float64")
    return df_oportunidades.groupby("estagio_funil")["valor_estimado"].sum().sort_values(ascending=False)


def taxa_conversao_funil(df_oportunidades: pd.DataFrame, estagio_ganho="Ganho") -> float:
    """% de oportunidades que chegaram no estágio de fechamento (ganho)."""
    if df_oportunidades.empty:
        return 0.0
    total = len(df_oportunidades)
    ganhas = (df_oportunidades["estagio_funil"] == estagio_ganho).sum()
    return round((ganhas / total) * 100, 2) if total else 0.0


def faturamento_por_mes(df_pagamentos: pd.DataFrame) -> pd.Series:
    if df_pagamentos.empty:
        return pd.Series(dtype="float64")
    serie = df_pagamentos.groupby("mes_referencia")["valor_total"].sum().sort_index()
    return serie


def faturamento_por_metodo_pagamento(df_pagamentos: pd.DataFrame) -> pd.Series:
    if df_pagamentos.empty:
        return pd.Series(dtype="float64")
    return df_pagamentos.groupby("metodo_pagamento")["valor_total"].sum().sort_values(ascending=False)


def avaliacao_media_por_parceiro(df_avaliacoes: pd.DataFrame, top_n: int = 10) -> pd.Series:
    if df_avaliacoes.empty:
        return pd.Series(dtype="float64")
    media = df_avaliacoes.groupby("razao_social")["nota"].mean().round(2)
    return media.sort_values(ascending=False).head(top_n)


def viagens_por_status(df_viagens: pd.DataFrame) -> pd.Series:
    if df_viagens.empty:
        return pd.Series(dtype="int64")
    return df_viagens.groupby("status_viagem").size().sort_values(ascending=False)


def viagens_por_mes(df_viagens: pd.DataFrame) -> pd.Series:
    if df_viagens.empty:
        return pd.Series(dtype="int64")
    return df_viagens.groupby("mes_embarque").size().sort_index()

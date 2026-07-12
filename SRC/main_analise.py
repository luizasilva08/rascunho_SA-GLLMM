"""
main_analise.py — linha de controle e automação da análise de dados do
LuxeVoyage (o equivalente ao notebook de exemplo, só que automatizado
ponta a ponta e puxando direto do banco em vez de um CSV manual).

Pipeline, pra cada análise:
    1. coleta   -> busca os dados brutos no banco
    2. trata    -> limpa/padroniza
    3. calcula  -> agrupa/resume (métricas)
    4. plota    -> gera e salva o gráfico em saida/graficos/

Rode a partir da pasta raiz do projeto:

    python main_analise.py

No final, os dados tratados também são exportados como CSV em
saida/dados_tratados/ — úteis pra abrir no Excel ou anexar num relatório.
"""
import os
import sys
import pathlib

# --- bootstrap de caminho ---------------------------------------------------
# analise/ mora em TEST/ (pasta irmã de SRC/), não dentro de SRC/. Sem isso,
# `from analise import coleta` não seria encontrado.
_RAIZ_PROJETO = pathlib.Path(__file__).resolve().parent.parent
_PASTA_TEST = _RAIZ_PROJETO / "TEST"
if str(_PASTA_TEST) not in sys.path:
    sys.path.insert(0, str(_PASTA_TEST))
# -----------------------------------------------------------------------------

from analise import coleta, tratamento, metricas, graficos

PASTA_DADOS_TRATADOS = os.path.join("saida", "dados_tratados")


def _log_etapa(texto):
    print(f"\n>>> {texto}")


def _exportar_csv(df, nome_arquivo):
    if df is None or df.empty:
        return None
    os.makedirs(PASTA_DADOS_TRATADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS_TRATADOS, nome_arquivo)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    return caminho


def analisar_clientes():
    _log_etapa("Clientes: coletando, tratando e gerando gráfico...")
    df = tratamento.tratar_clientes(coleta.extrair_clientes())
    _exportar_csv(df, "clientes_tratado.csv")
    serie = metricas.clientes_por_estado(df)
    caminho = graficos.grafico_clientes_por_estado(serie)
    if caminho:
        print(f"  gráfico salvo em: {caminho}")
    return df, serie


def analisar_pacotes():
    _log_etapa("Pacotes: coletando, tratando e gerando gráficos...")
    df = tratamento.tratar_pacotes(coleta.extrair_pacotes())
    _exportar_csv(df, "pacotes_tratado.csv")

    serie_status = metricas.pacotes_por_status(df)
    caminho1 = graficos.grafico_pacotes_por_status(serie_status)
    if caminho1:
        print(f"  gráfico salvo em: {caminho1}")

    serie_destino = metricas.pacotes_por_destino(df)
    caminho2 = graficos.grafico_pacotes_por_destino(serie_destino)
    if caminho2:
        print(f"  gráfico salvo em: {caminho2}")

    return df, serie_status, serie_destino


def analisar_funil_vendas():
    _log_etapa("Funil de vendas (CRM): coletando, tratando e gerando gráficos...")
    df = tratamento.tratar_oportunidades(coleta.extrair_oportunidades())
    _exportar_csv(df, "oportunidades_tratado.csv")

    serie_estagio = metricas.oportunidades_por_estagio(df)
    caminho1 = graficos.grafico_funil_oportunidades(serie_estagio)
    if caminho1:
        print(f"  gráfico salvo em: {caminho1}")

    serie_valor = metricas.valor_estimado_por_estagio(df)
    caminho2 = graficos.grafico_valor_por_estagio(serie_valor)
    if caminho2:
        print(f"  gráfico salvo em: {caminho2}")

    taxa = metricas.taxa_conversao_funil(df)
    print(f"  taxa de conversão (estágio 'Ganho'): {taxa}%")

    return df, serie_estagio, serie_valor, taxa


def analisar_financeiro():
    _log_etapa("Financeiro: coletando pagamentos, tratando e gerando gráficos...")
    df = tratamento.tratar_pagamentos(coleta.extrair_pagamentos())
    _exportar_csv(df, "pagamentos_tratado.csv")

    serie_mensal = metricas.faturamento_por_mes(df)
    caminho1 = graficos.grafico_faturamento_mensal(serie_mensal)
    if caminho1:
        print(f"  gráfico salvo em: {caminho1}")

    serie_metodo = metricas.faturamento_por_metodo_pagamento(df)
    caminho2 = graficos.grafico_faturamento_por_metodo(serie_metodo)
    if caminho2:
        print(f"  gráfico salvo em: {caminho2}")

    total = df["valor_total"].sum() if not df.empty else 0
    print(f"  faturamento total (pagamentos coletados): R$ {total:,.2f}")

    return df, serie_mensal, serie_metodo


def analisar_parceiros():
    _log_etapa("Parceiros: coletando avaliações, tratando e gerando gráfico...")
    df = tratamento.tratar_avaliacoes(coleta.extrair_avaliacoes())
    _exportar_csv(df, "avaliacoes_tratado.csv")
    serie = metricas.avaliacao_media_por_parceiro(df)
    caminho = graficos.grafico_avaliacao_parceiros(serie)
    if caminho:
        print(f"  gráfico salvo em: {caminho}")
    return df, serie


def analisar_viagens():
    _log_etapa("Viagens: coletando, tratando e gerando gráficos...")
    df = tratamento.tratar_viagens(coleta.extrair_viagens())
    _exportar_csv(df, "viagens_tratado.csv")

    serie_status = metricas.viagens_por_status(df)
    caminho1 = graficos.grafico_viagens_por_status(serie_status)
    if caminho1:
        print(f"  gráfico salvo em: {caminho1}")

    serie_mes = metricas.viagens_por_mes(df)
    caminho2 = graficos.grafico_viagens_por_mes(serie_mes)
    if caminho2:
        print(f"  gráfico salvo em: {caminho2}")

    return df, serie_status, serie_mes


def rodar_pipeline_completo():
    """Roda todas as análises em sequência — a automação de ponta a ponta."""
    print("############################################")
    print("#   LuxeVoyage — Pipeline de Análise de Dados #")
    print("############################################")

    resultados = {}
    etapas = [
        ("clientes", analisar_clientes),
        ("pacotes", analisar_pacotes),
        ("funil_vendas", analisar_funil_vendas),
        ("financeiro", analisar_financeiro),
        ("parceiros", analisar_parceiros),
        ("viagens", analisar_viagens),
    ]

    for nome, funcao in etapas:
        try:
            resultados[nome] = funcao()
        except Exception as e:
            print(f"  ❌ Erro na etapa '{nome}': {e}")
            resultados[nome] = None

    print("\n\n============================================")
    print("Pipeline concluído.")
    print(f"Gráficos salvos em: {graficos.PASTA_SAIDA}/")
    print(f"Dados tratados (CSV) salvos em: {PASTA_DADOS_TRATADOS}/")
    print("============================================")

    return resultados


if __name__ == "__main__":
    rodar_pipeline_completo()

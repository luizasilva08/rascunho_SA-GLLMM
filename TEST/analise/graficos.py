"""
analise/graficos.py — geração de gráficos (equivalente à célula
`grupado_genero.plot.bar(...)` do notebook original, só que uma função por
gráfico, e cada uma já salva o arquivo em vez de só mostrar na tela).
"""
import os
import matplotlib
matplotlib.use("Agg")  # gera as imagens sem precisar abrir janela
import matplotlib.pyplot as plt
import pandas as pd

PASTA_SAIDA = os.path.join("saida", "graficos")


def _preparar_pasta():
    os.makedirs(PASTA_SAIDA, exist_ok=True)


def _salvar(fig, nome_arquivo: str) -> str:
    _preparar_pasta()
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)
    fig.tight_layout()
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    return caminho


def grafico_barras(serie: pd.Series, titulo: str, eixo_x: str, eixo_y: str,
                    nome_arquivo: str, cor: str = "steelblue") -> str | None:
    """Gráfico de barras genérico — usado por várias análises."""
    if serie is None or serie.empty:
        print(f"  (sem dados para '{titulo}', gráfico não gerado)")
        return None
    fig, ax = plt.subplots(figsize=(9, 5))
    serie.plot.bar(ax=ax, color=cor)
    ax.set_title(titulo)
    ax.set_xlabel(eixo_x)
    ax.set_ylabel(eixo_y)
    plt.xticks(rotation=45, ha="right")
    return _salvar(fig, nome_arquivo)


def grafico_pizza(serie: pd.Series, titulo: str, nome_arquivo: str) -> str | None:
    """Gráfico de pizza genérico — bom pra proporções (ex: status)."""
    if serie is None or serie.empty:
        print(f"  (sem dados para '{titulo}', gráfico não gerado)")
        return None
    fig, ax = plt.subplots(figsize=(7, 7))
    serie.plot.pie(ax=ax, autopct="%1.1f%%", ylabel="")
    ax.set_title(titulo)
    return _salvar(fig, nome_arquivo)


def grafico_linha(serie: pd.Series, titulo: str, eixo_x: str, eixo_y: str,
                   nome_arquivo: str, cor: str = "darkorange") -> str | None:
    """Gráfico de linha genérico — bom pra séries temporais (ex: faturamento por mês)."""
    if serie is None or serie.empty:
        print(f"  (sem dados para '{titulo}', gráfico não gerado)")
        return None
    fig, ax = plt.subplots(figsize=(9, 5))
    serie.plot.line(ax=ax, marker="o", color=cor)
    ax.set_title(titulo)
    ax.set_xlabel(eixo_x)
    ax.set_ylabel(eixo_y)
    plt.xticks(rotation=45, ha="right")
    return _salvar(fig, nome_arquivo)


# ---------------------------------------------------------------------------
# Uma função por análise, já com título/eixos/nome de arquivo definidos —
# assim quem chama (main_analise.py) não precisa saber esses detalhes.
# ---------------------------------------------------------------------------
def grafico_clientes_por_estado(serie):
    return grafico_barras(serie, "Clientes por estado de origem", "UF", "Quantidade",
                           "clientes_por_estado.png", cor="steelblue")


def grafico_pacotes_por_status(serie):
    return grafico_pizza(serie, "Pacotes por status", "pacotes_por_status.png")


def grafico_pacotes_por_destino(serie):
    return grafico_barras(serie, "Destinos mais populares (top 10)", "Destino", "Nº de pacotes",
                           "pacotes_por_destino.png", cor="seagreen")


def grafico_funil_oportunidades(serie):
    return grafico_barras(serie, "Oportunidades por estágio do funil", "Estágio", "Quantidade",
                           "funil_oportunidades.png", cor="mediumpurple")


def grafico_valor_por_estagio(serie):
    return grafico_barras(serie, "Valor estimado por estágio do funil (R$)", "Estágio", "R$",
                           "valor_por_estagio.png", cor="indianred")


def grafico_faturamento_mensal(serie):
    return grafico_linha(serie, "Faturamento por mês (R$)", "Mês", "R$",
                          "faturamento_mensal.png")


def grafico_faturamento_por_metodo(serie):
    return grafico_pizza(serie, "Faturamento por método de pagamento", "faturamento_por_metodo.png")


def grafico_avaliacao_parceiros(serie):
    return grafico_barras(serie, "Avaliação média por parceiro (top 10)", "Parceiro", "Nota média",
                           "avaliacao_parceiros.png", cor="goldenrod")


def grafico_viagens_por_status(serie):
    return grafico_pizza(serie, "Viagens por status", "viagens_por_status.png")


def grafico_viagens_por_mes(serie):
    return grafico_linha(serie, "Viagens por mês de embarque", "Mês", "Quantidade",
                          "viagens_por_mes.png", cor="teal")

# Análise de Dados — LuxeVoyage

Inspirado no notebook de exemplo (WEG): ler dados → tratar → agrupar →
gerar gráfico. Só que aqui puxa direto do banco (em vez de CSV manual) e
é 100% automatizado — um `python main_analise.py` gera tudo de novo.

## Como rodar

```bash
pip install -r requirements.txt
python main_analise.py
```

Isso cria (ou atualiza) duas pastas na raiz do projeto:

```
saida/
    graficos/         -> 9 gráficos em PNG
        clientes_por_estado.png
        pacotes_por_status.png
        pacotes_por_destino.png
        funil_oportunidades.png
        valor_por_estagio.png
        faturamento_mensal.png
        faturamento_por_metodo.png
        avaliacao_parceiros.png
        viagens_por_status.png
        viagens_por_mes.png
    dados_tratados/    -> os mesmos dados, já tratados, em CSV
        clientes_tratado.csv
        pacotes_tratado.csv
        oportunidades_tratado.csv
        pagamentos_tratado.csv
        avaliacoes_tratado.csv
        viagens_tratado.csv
```

## Estrutura (pipeline em 4 etapas, por análise)

```
analise/
    coleta.py       -> ETAPA 1: busca dados brutos no banco (SQL -> DataFrame)
    tratamento.py   -> ETAPA 2: limpa/padroniza (tipos, nulos, texto)
    metricas.py     -> ETAPA 3: agrupa/calcula (groupby, médias, taxas)
    graficos.py     -> ETAPA 4: gera e salva os gráficos (matplotlib)

main_analise.py     -> orquestra as 4 etapas pra cada análise (a "linha de
                        controle" que dá nome ao pipeline)
```

Cada arquivo tem uma responsabilidade só — se um dia você quiser trocar de
matplotlib pra plotly, só mexe em `graficos.py`; se quiser mudar a query de
algum dado, só mexe em `coleta.py`. As outras camadas não são afetadas.

## Análises incluídas

| Análise | Métrica | Gráfico |
|---|---|---|
| Clientes | por estado (UF) de origem | barras |
| Pacotes | por status | pizza |
| Pacotes | destinos mais populares (top 10) | barras |
| Funil de vendas | oportunidades por estágio | barras |
| Funil de vendas | valor estimado por estágio | barras |
| Funil de vendas | taxa de conversão (%) | impresso no terminal |
| Financeiro | faturamento por mês | linha |
| Financeiro | faturamento por método de pagamento | pizza |
| Parceiros | avaliação média (top 10) | barras |
| Viagens | por status | pizza |
| Viagens | por mês de embarque | linha |

## Adicionando uma análise nova

1. Adicione uma função de coleta em `coleta.py` (retorna um DataFrame).
2. Adicione uma função de tratamento em `tratamento.py`.
3. Adicione uma função de métrica em `metricas.py` (retorna Series/DataFrame resumido).
4. Adicione uma função de gráfico em `graficos.py` (chame `grafico_barras`,
   `grafico_pizza` ou `grafico_linha`, que já cuidam de salvar o arquivo).
5. Adicione uma função `analisar_x()` em `main_analise.py` juntando as 4
   etapas, e inclua-a na lista `etapas` de `rodar_pipeline_completo()`.

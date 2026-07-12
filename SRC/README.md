# LuxeVoyage — CRUD + Site (Streamlit)

Backend modularizado (um módulo por tabela, 25 no total, organizados em 8
pastas por domínio) com **duas interfaces diferentes** por cima dele:

- `main.py` — menu interativo no terminal
- `app.py` — site interativo (Streamlit), navegador

As duas usam exatamente a mesma lógica de CRUD — nenhum código foi duplicado.

## Estrutura

```
database.py     -> conexão com o banco (lê credenciais do .env)
utils.py        -> execute_query() e build_update_clause() (usados por todos os módulos)
registro.py     -> registro central: domínio -> tabela -> metadados
                    (fonte única de verdade, usada por main.py E por app.py)

main.py         -> menu de terminal
app.py          -> site (streamlit run app.py)

geografia/, parceiros/, catalogo/, clientes/, crm/, comercial/,
operacional/, auditoria/
                -> os 25 módulos de tabela (sem nenhuma mudança em relação
                   à versão anterior — só ganharam uma segunda interface)

frontend/
    componentes.py      -> componentes de UI genéricos do site
                            (Listar / Criar / Buscar-Editar / Deletar / Buscar por campo)
    paginas/
        home_page.py         -> dashboard (métricas + gráficos)
        geografia_page.py    -> uma página por domínio (chama componentes.py)
        parceiros_page.py
        catalogo_page.py
        clientes_page.py
        crm_page.py
        comercial_page.py
        operacional_page.py
        auditoria_page.py
        sql_page.py           -> consulta SQL livre (somente SELECT)

.env / .env.example / .gitignore / requirements.txt
```

## Como o site reaproveita o CRUD existente

`frontend/componentes.py` tem funções genéricas (`render_dominio`,
`render_tabela`) que recebem os metadados de `registro.py` (mesmo dict do
menu de terminal) e, a partir do nome da entidade, chamam dinamicamente as
funções que já existiam nos módulos (`criar_x`, `buscar_x_por_id`,
`listar_xs`, etc.) via `getattr`. Cada página de domínio
(`frontend/paginas/*.py`) tem só 6 linhas — ela apenas busca o domínio dela
em `REGISTRO` e delega a renderização.

Se um dia você adicionar uma tabela nova, só precisa:

1. Criar o módulo de CRUD dela (seguindo o padrão das outras).
2. Cadastrar em `registro.py`.

Isso já é suficiente pra ela aparecer tanto no menu de terminal quanto no site.

## Rodando

```bash
pip install -r requirements.txt

# menu de terminal
python main.py

# site
streamlit run app.py
```

O `streamlit run app.py` abre automaticamente no navegador
(`http://localhost:8501`). A navegação lateral tem:

- **Dashboard** — métricas gerais e gráficos
- **Domínios** — Geografia, Parceiros, Catálogo, Clientes, CRM, Comercial,
  Operacional, Auditoria (cada um com um seletor de tabela e abas de
  Listar / Criar / Buscar-Editar / Deletar / Buscar por campo)
- **Consulta SQL** — SELECT livre

## Conexão

Configure o `.env` (copie de `.env.example`) com as credenciais do Aiven.
Esse arquivo nunca vai pro Git (já está no `.gitignore`).

""" Do you want to install the recommended 'Rainbow CSV' extension from mechatroner for avaliacoes_tratado.csv? """

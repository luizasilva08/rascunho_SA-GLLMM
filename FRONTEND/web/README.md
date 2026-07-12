# LuxeVoyage — Site HTML/CSS/JS

Novo front-end do LuxeVoyage, escrito em **HTML + CSS + JavaScript puro**
(sem framework), interativo com o banco de dados MySQL do projeto através
de uma API REST em Flask (`SRC/api_server.py`).

Ele **reaproveita 100% da camada de dados que já existe** no projeto
(`registro.py`, `utils.py`, e todos os módulos CRUD em `TEST/`) — não
duplica nenhuma regra de negócio. A API só expõe, em JSON, as mesmas
funções que o menu de terminal (`main.py`) e o site Streamlit (`app.py`)
já usam.

## Estrutura

```
SRC/api_server.py          -> backend Flask (API REST + serve o site)
FRONTEND/web/index.html    -> página única (SPA)
FRONTEND/web/css/style.css -> todo o estilo visual
FRONTEND/web/js/api.js     -> camada de comunicação com a API (fetch)
FRONTEND/web/js/app.js     -> roteamento, menu, dashboard, CRUD, SQL
```

## Como rodar

```bash
cd SRC
pip install -r requirements.txt
python api_server.py
```

Abra **http://localhost:5000** no navegador. Você também pode chegar até
aqui pelo menu principal do projeto:

```bash
python main.py
# opção 3. Abrir novo site (HTML/CSS/JS + Flask)
```

Lembre-se de configurar o `.env` (veja `SRC/.env.example`) com as
credenciais do banco antes de rodar.

## O que o site tem

- **Menu lateral** montado dinamicamente a partir de `registro.py`
  (endpoint `/api/registro`) — os mesmos 8 domínios do menu de terminal
  e do Streamlit: Geografia, Parceiros, Catálogo, Clientes, CRM,
  Comercial, Operacional e Auditoria. Qualquer tabela nova cadastrada em
  `registro.py` aparece no site automaticamente, sem tocar em nenhum
  arquivo de front-end.
- **Dashboard** com as mesmas métricas e gráficos do `home_page.py`
  (clientes, pacotes, parceiros, viagens, oportunidades por estágio do
  funil, viagens por status).
- **CRUD completo por tabela**: listar com paginação, buscar por campo,
  criar, editar e excluir — via modal, sem recarregar a página.
- **Consulta SQL livre** (somente `SELECT`, igual à opção 9 do menu de
  terminal).
- Sem dependências externas de JS (nenhuma lib de terceiros) — só
  `fetch()` nativo e DOM.

## Endpoints da API

| Método | Rota                                   | Ação                                   |
|--------|-----------------------------------------|-----------------------------------------|
| GET    | `/api/registro`                         | estrutura de domínios/tabelas           |
| GET    | `/api/dashboard`                        | métricas + gráficos da home             |
| GET    | `/api/<dominio>/<tabela>`               | listar (paginado) ou buscar por campo   |
| GET    | `/api/<dominio>/<tabela>/<id>`          | buscar um registro por id               |
| POST   | `/api/<dominio>/<tabela>`               | criar registro                          |
| PUT    | `/api/<dominio>/<tabela>/<id>`          | atualizar registro                      |
| DELETE | `/api/<dominio>/<tabela>/<id>`          | excluir registro                        |
| POST   | `/api/sql`                              | consulta SQL livre (somente SELECT)     |

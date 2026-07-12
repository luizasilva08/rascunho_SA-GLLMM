# ✈️ Luxe Voyage — Sistema de Expansão Nacional

> Reestruturação do modelo de dados e construção do sistema completo para operação em escala nacional, 100% remota e digital.

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Versão](https://img.shields.io/badge/versão-1.0-green)
![Banco](https://img.shields.io/badge/banco-MySQL%20(Aiven)-4479A1)
![Python](https://img.shields.io/badge/python-3.12+-3776AB)
![Streamlit](https://img.shields.io/badge/site-Streamlit-FF4B4B)

---

## Sobre o projeto

A **Luxe Voyage** é uma agência de viagens que operava exclusivamente no litoral Sul e Sudeste. Este projeto reestruturou o sistema de dados para suportar uma operação nacional cobrindo todos os **26 estados e o Distrito Federal**, sem abertura de filiais físicas, e entregou o sistema completo: banco de dados, CRUD, site interativo, pipeline de análise de dados e envio automático de relatórios por e-mail.

A expansão é sustentada por quatro pilares estruturais que guiam toda a modelagem do banco de dados e as funcionalidades do sistema.

| Métrica | Valor |
|---|---|
| Tabelas no banco | 25 |
| Domínios de negócio | 8 |
| Requisitos funcionais | 22 |
| Requisitos não funcionais | 7 |
| Estados cobertos | 27 (26 UFs + DF) |

---

## Pilares do sistema

### P1 — Hierarquia geográfica nacional
Malha geográfica completa com estados e municípios categorizados entre **capitais** e **cidades turísticas principais**. Filtros regionais por Norte, Nordeste, Centro-Oeste, Sudeste e Sul. Marcação de destinos sazonais por período.

### P2 — Rede de parceiros terceirizados
Cadastro de **Operadoras Nacionais** e **Receptivos Locais/DMCs** com área de cobertura mapeada por município. Vínculo automático entre parceiro e destino no momento da criação de pacotes.

### P3 — Pacotes modulares de viagem
Composição dinâmica de pacotes por módulos independentes (hotel, passeio, transfer, aéreo). Precificação automática por sazonalidade regional (baixa, média, alta).

### P4 — Rastreabilidade de clientes
Base de clientes interestadual com **UF de origem obrigatória**, histórico completo de interações, envio de proposta 100% digital e contrato com **aceite eletrônico** (timestamp + registro de IP).

---

## O que foi entregue

- **Banco de dados relacional** com 25 tabelas (MySQL, hospedado no Aiven Cloud), cobrindo geografia, parceiros, catálogo de pacotes, clientes, CRM, comercial, operacional e auditoria.
- **CRUD completo** — um módulo Python por tabela, todos seguindo o mesmo padrão (`criar_x`, `buscar_x_por_id`, `listar_x`, `buscar_x_por_campo`, `atualizar_x`, `deletar_x`).
- **Menu interativo no terminal** — navega pelas 25 tabelas por domínio, sem precisar escrever SQL na mão.
- **Site interativo (Streamlit)** — a mesma navegação do terminal, só que num navegador, com dashboard e gráficos.
- **Pipeline de análise de dados** — coleta, trata, calcula métricas e gera gráficos automaticamente a partir do banco (clientes por estado, funil de vendas, faturamento, avaliação de parceiros, etc.).
- **Relatório automático por e-mail** — gera os gráficos/CSVs mais recentes, compacta em `.zip` e envia por e-mail via API oficial do Gmail (OAuth 2.0), sem precisar abrir nada manualmente.
- **Um único ponto de entrada** (`main.py`) reunindo as 4 funcionalidades acima num menu.

---

## Arquitetura do projeto

O projeto é dividido em pastas por responsabilidade — separando código-fonte, lógica de domínio, interface web e dados/documentação:

```
SA-MA78-GLLMM/
├── SRC/                    → ponto de entrada do sistema
│   ├── main.py                  → menu principal (hub: CRUD / site / análise / e-mail)
│   ├── app.py                    → site Streamlit
│   ├── main_analise.py           → pipeline de análise de dados
│   ├── database.py               → conexão com o MySQL (lê credenciais do .env)
│   ├── utils.py                  → execução de queries (usado por todo o CRUD)
│   ├── registro.py               → registro central: domínio → tabela → metadados
│   ├── test_connection.py        → testa a conexão com o banco isoladamente
│   ├── requirements.txt
│   ├── .env / .env.example       → credenciais (o .env real nunca vai pro Git)
│   └── .gitignore
│
├── TEST/                    → módulos de domínio (a "camada de dados" do sistema)
│   ├── geografia/                → Estado, Municipio
│   ├── parceiros/                 → Parceiros, Cobertura, Serviços, Avaliações
│   ├── catalogo/                  → Pacote, Temporada, Módulos, Preço Sazonal, Destaques
│   ├── clientes/                  → Cliente, Interesses, Consentimentos LGPD
│   ├── crm/                       → Usuário Interno, Oportunidade, Interações, SLA
│   ├── comercial/                 → Cotação, Item, Proposta, Contrato Digital
│   ├── operacional/                → Viagem, Pagamento
│   ├── auditoria/                  → Log de Acesso
│   └── analise/                    → coleta, tratamento, métricas, gráficos e envio de e-mail
│       ├── coleta.py                    → busca dados brutos no banco (SQL → DataFrame)
│       ├── tratamento.py                → limpeza/padronização (tipos, nulos, texto)
│       ├── metricas.py                  → agrupamentos e cálculos (groupby, médias, taxas)
│       ├── graficos.py                  → geração dos gráficos (matplotlib)
│       ├── gmail_api.py                 → envio de e-mail via API do Gmail (OAuth 2.0)
│       └── email_relatorio.py           → monta e dispara o relatório por e-mail
│
├── FRONTEND/                → site (Streamlit)
│   ├── componentes.py            → componentes de UI genéricos (Listar/Criar/Editar/Deletar)
│   └── paginas/                   → uma página por domínio + Dashboard + Consulta SQL
│
├── DATA/                    → scripts SQL do banco (DDL e inserts, por bloco de entrega)
└── DOCS/                    → documentação complementar do projeto
```

> **Por que `SRC`, `TEST` e `FRONTEND` são pastas irmãs?** Cada arquivo de entrada
> (`main.py`, `app.py`, `main_analise.py`) faz um pequeno ajuste de `sys.path` no
> topo, ensinando o Python a enxergar as pastas vizinhas. Isso permite manter a
> separação de responsabilidades (código de entrada / lógica de domínio /
> interface web) sem duplicar nada.

---

## Tecnologias

### Banco de dados
- MySQL 8.0+ (hospedado no **Aiven Cloud**)
- Conexão criptografada (SSL)
- Engine InnoDB (suporte a transações e chaves estrangeiras)
- 25 tabelas normalizadas, com integridade referencial completa

### Back-end
- **Python 3.12+**
- `mysql-connector-python` — conexão com o banco
- `python-dotenv` — carregamento de credenciais via `.env`
- Arquitetura modular: um módulo por tabela, agrupados por domínio de negócio

### Site / Dashboard
- **Streamlit** — navegação multi-página, formulários de CRUD e gráficos interativos
- **pandas** — manipulação tabular dos resultados

### Análise de dados
- **pandas** — tratamento e agrupamento dos dados
- **matplotlib** — geração dos gráficos (barras, pizza, linha)
- Exportação automática de CSVs tratados e PNGs prontos para relatório

### Automação / Integrações
- **Gmail API (OAuth 2.0)** — envio automático de relatórios por e-mail, sem senha armazenada em texto puro
- Pipeline ponta a ponta: banco → tratamento → gráfico → `.zip` → e-mail, com um único comando

---

## Estrutura do banco de dados (por domínio)

```
Geografia     → Estado, Municipio
Parceiros     → Parceiros, Cobertura_Parceiros, Servicos_Parceiros, Avaliacoes_Parceiros
Catálogo      → Pacote, Temporada, Modulos_Pacote, Preco_Sazonal, Destaques_Sazonais
Clientes      → Cliente, Interesses_Cliente, Consentimentos_LGPD
CRM           → Usuario_Interno, Oportunidade_CRM, Historico_Interacoes, Solicitacao_SLA
Comercial     → Cotacao_Personalizadas, Item_Cotacao, Propostas_Comerciais, Contrato_Digital
Operacional   → Viagem, Pagamento_Contrato
Auditoria     → Log_Acesso
```

Os scripts de criação (`DDL`) e os inserts de exemplo ficam em `DATA/`, organizados por bloco de entrega do projeto.

---

## Como rodar

### 1. Pré-requisitos
```bash
cd SRC
pip install -r requirements.txt
```

### 2. Configurar a conexão com o banco
Copie `SRC/.env.example` para `SRC/.env` e preencha com suas credenciais do Aiven:
```
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...
```

### 3. (Opcional) Configurar o envio de e-mail
Para usar a opção de relatório por e-mail, é preciso:
1. Criar um projeto no [Google Cloud Console](https://console.cloud.google.com) e ativar a **Gmail API**.
2. Gerar credenciais OAuth do tipo "Aplicativo de desktop" e baixar o JSON.
3. Renomear para `credentials.json` e colocar dentro de `SRC/` (mesma pasta do `main.py`).
4. Preencher no `.env`:
   ```
   EMAIL_REMETENTE=seu-email@dominio.com
   EMAIL_DESTINATARIO=destinatario@dominio.com
   ```

Na primeira execução, uma aba do navegador vai pedir login — depois disso, o token fica salvo (`SRC/token.json`) e não pede de novo.

### 4. Rodar o sistema
```bash
cd SRC
python main.py
```

Isso abre o menu principal:
```
1. Menu CRUD (terminal)
2. Abrir site (Streamlit)
3. Rodar análise de dados (gráficos + CSVs)
4. Enviar relatório por e-mail (CSV + PNG) ao supervisor
0. Sair
```

---

## Requisitos funcionais (resumo)

| Pilar | IDs | Quantidade |
|---|---|---|
| Hierarquia geográfica | RF-01 a RF-05 | 5 |
| Rede de parceiros | RF-06 a RF-10 | 5 |
| Pacotes modulares | RF-11 a RF-16 | 6 |
| Rastreabilidade de clientes | RF-17 a RF-22 | 6 |

## Requisitos não funcionais (resumo)

| ID | Categoria | Meta |
|---|---|---|
| RNF-01 | Tempo de resposta | < 2 segundos para buscas e filtros |
| RNF-02 | Escalabilidade horizontal | Novas instâncias sem reescrever o sistema |
| RNF-03 | Organização por domínio | Módulos isolados por área de negócio |
| RNF-04 | Criptografia e mascaramento | Dados sensíveis do cliente armazenados de forma protegida |
| RNF-05 | LGPD | Consentimento, anonimização e exclusão a pedido |
| RNF-06 | Backups | Responsabilidade do provedor de banco (Aiven) |
| RNF-07 | Alta disponibilidade | Banco hospedado em nuvem (Aiven Cloud) |

---

## Segurança e conformidade (LGPD)

- CPF, e-mail e telefone armazenados de forma protegida (colunas `_criptografado`)
- Contratos digitais com timestamp de aceite, IP registrado e hash de integridade
- Consentimento de uso (LGPD) registrado por cliente, com status auditável
- Log de acesso registrando cada operação feita por usuários internos
- Credenciais (banco de dados e Gmail API) nunca ficam no código — só em `.env`, `credentials.json` e `token.json`, todos fora do controle de versão (`.gitignore`)

---

## Stakeholders

### Internos
| Nome | Papel | Prioridade no projeto |
|---|---|---|
| Ricardo Almeida | Sócio fundador e diretor geral | Manter qualidade do atendimento na migração |
| Patrícia Costa | Sócia e diretora comercial | Painel de gestão centralizado por região |
| Fernando Matos | Sócio e responsável financeiro | Controle de custos de infraestrutura |

### Externos (clientes)
| Nome | Perfil | Necessidade |
|---|---|---|
| Ana Souza, 36 — Porto Alegre | Cliente fiel | Histórico e cotação self-service pelo celular |
| Thiago Ribeiro, 44 — Goiânia | Cliente potencial | Preço estimado visível sem entrar em contato |
| Juliana Lima, 29 — Recife | Cliente potencial | Contrato digital sem papel |

---

*Luxe Voyage · Projeto de expansão nacional · v1.0 · Concluído*

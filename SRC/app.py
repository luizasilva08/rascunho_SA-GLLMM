"""
app.py — ponto de entrada do site (Streamlit) do LuxeVoyage.

Rode a partir da pasta SRC/:

    cd SRC
    streamlit run app.py

Estrutura (pastas SEPARADAS, lado a lado da raiz do projeto):
    SRC/app.py                   -> este arquivo
    FRONTEND/componentes.py       -> componentes de UI genéricos (Listar/Criar/Editar/Deletar)
    FRONTEND/paginas/*.py         -> uma página por domínio + Dashboard + Consulta SQL

Como FRONTEND/ é uma pasta IRMÃ de SRC/ (não uma subpasta), os caminhos do
st.Page() abaixo usam "../FRONTEND/..." pra subir um nível e entrar nela.

Cada página em FRONTEND/paginas/ é "burra" de propósito: ela só busca o
domínio dela em REGISTRO e delega a renderização pra componentes.render_dominio().
Toda a lógica de CRUD em si já existe nos módulos de tabela (TEST/geografia/,
TEST/clientes/, etc.) — o site não duplica nada, só oferece outra forma de
usar o mesmo backend do main.py.
"""
import streamlit as st


st.set_page_config(page_title="LuxeVoyage", page_icon="🧳", layout="wide")

paginas = {
    "Início": [
        st.Page("../FRONTEND/paginas/home_page.py", title="Dashboard", icon="🏠", default=True),
    ],
    "Domínios": [
        st.Page("../FRONTEND/paginas/geografia_page.py", title="Geografia", icon="🌎"),
        st.Page("../FRONTEND/paginas/parceiros_page.py", title="Parceiros", icon="🤝"),
        st.Page("../FRONTEND/paginas/catalogo_page.py", title="Catálogo", icon="🧳"),
        st.Page("../FRONTEND/paginas/clientes_page.py", title="Clientes", icon="👤"),
        st.Page("../FRONTEND/paginas/crm_page.py", title="CRM", icon="📈"),
        st.Page("../FRONTEND/paginas/comercial_page.py", title="Comercial", icon="💼"),
        st.Page("../FRONTEND/paginas/operacional_page.py", title="Operacional", icon="✈️"),
        st.Page("../FRONTEND/paginas/auditoria_page.py", title="Auditoria", icon="🛡️"),
    ],
    "Ferramentas": [
        st.Page("../FRONTEND/paginas/sql_page.py", title="Consulta SQL", icon="🛠️"),
    ],
}

pagina_atual = st.navigation(paginas)
pagina_atual.run()

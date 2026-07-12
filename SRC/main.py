"""
main.py — ponto de entrada ÚNICO do projeto LuxeVoyage.

Rode a partir da pasta raiz do projeto:

    python main.py

Ao rodar, você escolhe entre 3 caminhos (tudo no mesmo arquivo, sem
precisar lembrar de rodar app.py ou main_analise.py separadamente):

    1. Menu CRUD no terminal (navega pelas 25 tabelas, domínio por domínio)
    2. Site (Streamlit) — abre app.py num processo separado, no navegador
    3. Pipeline de análise de dados — roda main_analise.py, gera os
       gráficos em saida/graficos/ e os CSVs tratados em saida/dados_tratados/

Usa o registro central de tabelas (registro.py) e o utils.execute_query()
para consultas SQL livres. O mesmo registro também é usado pelo site
(app.py / frontend/), então qualquer tabela nova só precisa ser cadastrada
uma vez, em registro.py.
"""

import sys
import pathlib

# --- bootstrap de caminho ---------------------------------------------------
# Este arquivo (main.py) mora em SRC/. Os módulos de domínio (geografia/,
# clientes/, analise/, etc.) moram numa pasta IRMÃ chamada TEST/. Sem essa
# linha, `from geografia import estado` (e também `from analise.email_relatorio
# import ...`) não seriam encontrados.
_RAIZ_PROJETO = pathlib.Path(__file__).resolve().parent.parent
_PASTA_TEST = _RAIZ_PROJETO / "TEST"
if str(_PASTA_TEST) not in sys.path:
    sys.path.insert(0, str(_PASTA_TEST))
# -----------------------------------------------------------------------------

from utils import execute_query
from registro import REGISTRO



# ---------------------------------------------------------------------------
# Helpers de exibição
# ---------------------------------------------------------------------------
def imprimir_registros(registros):
    """Imprime uma lista de dicts (linhas do banco) em formato de tabela simples."""
    if not registros:
        print("(nenhum registro encontrado)")
        return
    colunas = list(registros[0].keys())
    larguras = [max(len(str(c)), *(len(str(r.get(c, ""))) for r in registros)) for c in colunas]

    def linha(valores):
        return " | ".join(str(v).ljust(w) for v, w in zip(valores, larguras))

    print(linha(colunas))
    print("-+-".join("-" * w for w in larguras))
    for r in registros:
        print(linha([r.get(c, "") for c in colunas]))
    print(f"\n({len(registros)} registro(s))")


def ler_valor(campo, obrigatorio=True):
    """Lê um valor do terminal. Enter vazio vira None (útil pra update parcial)."""
    valor = input(f"  {campo}: ").strip()
    if valor == "":
        return None
    return valor


def pausa():
    input("\nPressione Enter para continuar...")


# ---------------------------------------------------------------------------
# Operações genéricas (funcionam para qualquer tabela do REGISTRO)
# ---------------------------------------------------------------------------
def op_criar(info):
    print(f"\n--- Criar novo registro ---")
    valores = [ler_valor(c) for c in info["cols"]]
    funcao = getattr(info["mod"], f"criar_{info['entidade']}")
    try:
        novo_id = funcao(*valores)
        print(f"\n✅ Registro criado com sucesso! id gerado: {novo_id}")
    except Exception as e:
        print(f"\n❌ Erro ao criar registro: {e}")


def op_buscar_por_id(info):
    print(f"\n--- Buscar por id ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    funcao = getattr(info["mod"], f"buscar_{info['entidade']}_por_id")
    try:
        registro = funcao(id_valor)
        imprimir_registros([registro] if registro else [])
    except Exception as e:
        print(f"\n❌ Erro na busca: {e}")


def op_listar(info):
    print(f"\n--- Listar (paginado) ---")
    limit = input("  limite (Enter = 100): ").strip() or "100"
    offset = input("  offset (Enter = 0): ").strip() or "0"
    funcao = getattr(info["mod"], f"listar_{info['plural']}")
    try:
        registros = funcao(limit=int(limit), offset=int(offset))
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro ao listar: {e}")


def op_buscar_por_campo(info):
    print(f"\n--- Buscar por campo ---")
    print("  Colunas disponíveis:", ", ".join([info["pk"]] + info["cols"]))
    campo = input("  campo: ").strip()
    valor = input("  valor: ").strip()
    funcao = getattr(info["mod"], f"buscar_{info['plural']}_por_campo")
    try:
        registros = funcao(campo, valor)
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro na busca: {e}")


def op_atualizar(info):
    print(f"\n--- Atualizar registro ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    print("  Deixe em branco para não alterar um campo.")
    campos = {}
    for c in info["cols"]:
        valor = ler_valor(c, obrigatorio=False)
        if valor is not None:
            campos[c] = valor
    if not campos:
        print("\nNenhum campo informado, nada foi alterado.")
        return
    funcao = getattr(info["mod"], f"atualizar_{info['entidade']}")
    try:
        linhas = funcao(id_valor, **campos)
        print(f"\n✅ Atualização concluída. Linhas afetadas: {linhas}")
    except Exception as e:
        print(f"\n❌ Erro ao atualizar: {e}")


def op_deletar(info):
    print(f"\n--- Deletar registro ---")
    id_valor = input(f"  {info['pk']}: ").strip()
    confirmar = input(f"  Confirma a exclusão do id {id_valor}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Cancelado.")
        return
    funcao = getattr(info["mod"], f"deletar_{info['entidade']}")
    try:
        linhas = funcao(id_valor)
        print(f"\n✅ Exclusão concluída. Linhas afetadas: {linhas}")
    except Exception as e:
        print(f"\n❌ Erro ao deletar: {e}")


def op_sql_livre():
    print("\n--- Consulta SQL livre (somente SELECT) ---")
    query = input("  SQL> ").strip()
    if not query.lower().startswith("select"):
        print("Por segurança, esse modo aceita apenas comandos SELECT.")
        return
    try:
        registros = execute_query(query, fetch="all")
        imprimir_registros(registros)
    except Exception as e:
        print(f"\n❌ Erro na consulta: {e}")


OPERACOES = {
    "1": ("Criar", op_criar),
    "2": ("Buscar por id", op_buscar_por_id),
    "3": ("Listar (paginado)", op_listar),
    "4": ("Buscar por campo", op_buscar_por_campo),
    "5": ("Atualizar", op_atualizar),
    "6": ("Deletar", op_deletar),
}


# ---------------------------------------------------------------------------
# Menus de navegação
# ---------------------------------------------------------------------------
def menu_tabela(nome_tabela, info):
    while True:
        print(f"\n=== {nome_tabela} ===")
        for chave, (rotulo, _) in OPERACOES.items():
            print(f"  {chave}. {rotulo}")
        print("  0. Voltar")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            return
        if escolha in OPERACOES:
            _, funcao = OPERACOES[escolha]
            funcao(info)
            pausa()
        else:
            print("Opção inválida.")


def menu_dominio(nome_dominio, tabelas):
    while True:
        print(f"\n=== {nome_dominio} ===")
        nomes = list(tabelas.keys())
        for i, nome in enumerate(nomes, start=1):
            print(f"  {i}. {nome}")
        print("  0. Voltar")
        escolha = input("Escolha uma tabela: ").strip()

        if escolha == "0":
            return
        if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            nome_tabela = nomes[int(escolha) - 1]
            menu_tabela(nome_tabela, tabelas[nome_tabela])
        else:
            print("Opção inválida.")


def menu_crud():
    while True:
        print("\n############################################")
        print("#        LuxeVoyage — Menu CRUD              #")
        print("############################################")
        nomes = list(REGISTRO.keys())
        for i, nome in enumerate(nomes, start=1):
            print(f"  {i}. {nome}")
        print("  9. Consulta SQL livre (SELECT)")
        print("  0. Sair")
        escolha = input("Escolha um domínio: ").strip()

        if escolha == "0":
            print("Até logo!")
            break
        if escolha == "9":
            op_sql_livre()
            pausa()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
            nome_dominio = nomes[int(escolha) - 1]
            menu_dominio(nome_dominio, REGISTRO[nome_dominio])
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------------------
# Hub principal — ponto de entrada único do projeto.
# Escolhe entre o menu CRUD (terminal), o site (Streamlit) ou o pipeline
# de análise de dados. Cada opção usa o que já existe, sem duplicar nada.
# ---------------------------------------------------------------------------
def abrir_site():
    """Sobe o site Streamlit (app.py) num processo separado."""
    import subprocess
    import sys as _sys

    print("\nAbrindo o site no navegador (streamlit run app.py)...")
    print("Pra fechar o site, volte aqui e pressione Ctrl+C.\n")
    try:
        subprocess.run([_sys.executable, "-m", "streamlit", "run", "app.py"])
    except FileNotFoundError:
        print("❌ Streamlit não encontrado. Rode: pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\nSite encerrado.")


def abrir_site_html():
    """Sobe o novo site HTML/CSS/JS (api_server.py, Flask) num processo separado."""
    import subprocess
    import sys as _sys
    import webbrowser

    print("\nAbrindo o site em http://localhost:5000 (Flask + HTML/CSS/JS)...")
    print("Pra fechar o site, volte aqui e pressione Ctrl+C.\n")
    try:
        webbrowser.open("http://localhost:5000")
        subprocess.run([_sys.executable, "api_server.py"])
    except FileNotFoundError:
        print("❌ Flask não encontrado. Rode: pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\nSite encerrado.")


def rodar_analise():
    """Roda o pipeline de análise de dados (main_analise.py)."""
    try:
        from main_analise import rodar_pipeline_completo
        rodar_pipeline_completo()
    except Exception as e:
        print(f"\n❌ Erro ao rodar a análise de dados: {e}")


def enviar_relatorio_por_email():
    """Roda a análise (se preciso) e envia CSVs + gráficos por e-mail ao supervisor."""
    try:
        from analise.email_relatorio import enviar_relatorio_email
        enviar_relatorio_email()
    except Exception as e:
        print(f"\n❌ Erro ao enviar relatório por e-mail: {e}")


def menu_principal():
    while True:
        print("\n############################################")
        print("#           LuxeVoyage — Menu Principal      #")
        print("############################################")
        print("  1. Menu CRUD (terminal)")
        print("  2. Abrir site (Streamlit)")
        print("  3. Abrir novo site (HTML/CSS/JS + Flask)")
        print("  4. Rodar análise de dados (gráficos + CSVs)")
        print("  5. Enviar relatório por e-mail (CSV + PNG) ao supervisor")
        print("  0. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Até logo!")
            break
        elif escolha == "1":
            menu_crud()
        elif escolha == "2":
            abrir_site()
        elif escolha == "3":
            abrir_site_html()
        elif escolha == "4":
            rodar_analise()
            pausa()
        elif escolha == "5":
            enviar_relatorio_por_email()
            pausa()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()

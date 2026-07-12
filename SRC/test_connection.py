"""
test_connection.py — testa isoladamente a conexão com o Aiven,
sem passar pelo menu. Rode com:

    python test_connection.py
"""
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    import mysql.connector
except ImportError:
    print("❌ O pacote 'mysql-connector-python' não está instalado.")
    print("   Rode: pip install -r requirements.txt")
    raise SystemExit(1)

HOST = os.environ.get("DB_HOST")
PORT = int(os.environ.get("DB_PORT", "0") or 0)
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
DATABASE = os.environ.get("DB_NAME")

if not all([HOST, PORT, USER, PASSWORD, DATABASE]):
    print("❌ Faltam variáveis de ambiente. Crie um arquivo .env na raiz")
    print("   do projeto (copie de .env.example) com suas credenciais.")
    raise SystemExit(1)

print(f"Tentando conectar em {HOST}:{PORT}, banco '{DATABASE}', usuário '{USER}'...\n")

try:
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        ssl_disabled=False,
        connection_timeout=10,
    )
    print("✅ Conexão aberta com sucesso!")

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    versao = cursor.fetchone()
    print("Versão do MySQL:", versao[0])

    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    print(f"\n{len(tabelas)} tabela(s) encontrada(s):")
    for t in tabelas:
        print(" -", t[0])

    cursor.close()
    conn.close()
    print("\n✅ Teste concluído sem erros.")

except mysql.connector.Error as e:
    print("❌ Erro do MySQL ao conectar:")
    print(f"   Código: {e.errno}")
    print(f"   Mensagem: {e.msg}")
    traceback.print_exc()

except Exception:
    print("❌ Erro inesperado ao conectar:")
    traceback.print_exc()

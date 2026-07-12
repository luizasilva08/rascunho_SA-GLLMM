import os
import zipfile
import pathlib
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

PASTA_GRAFICOS = os.path.join("saida", "graficos")
PASTA_CSVS = os.path.join("saida", "dados_tratados")
PASTA_ZIPS = os.path.join("saida", "email_enviados")

# Pasta TEST/ (mesma pasta onde o gmail_api.py procura credentials.json/token.json)
_PASTA_TEST = pathlib.Path(__file__).resolve().parent.parent
_CREDENTIALS_JSON = _PASTA_TEST / "credentials.json"


def _listar_arquivos(pasta, extensao):
    if not os.path.isdir(pasta):
        return []
    return [
        os.path.join(pasta, nome)
        for nome in sorted(os.listdir(pasta))
        if nome.lower().endswith(extensao)
    ]


def _compactar_relatorio():
    csvs = _listar_arquivos(PASTA_CSVS, ".csv")
    pngs = _listar_arquivos(PASTA_GRAFICOS, ".png")
    if not csvs and not pngs:
        return None, []
    os.makedirs(PASTA_ZIPS, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    caminho_zip = os.path.join(PASTA_ZIPS, f"relatorio_luxevoyage_{timestamp}.zip")
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for arquivo in csvs + pngs:
            zf.write(arquivo, arcname=os.path.basename(arquivo))
    return caminho_zip, csvs + pngs


def _enviar_via_oauth(remetente, destinatario, assunto, corpo, caminho_zip):
    """Usa a API do Gmail com OAuth 2.0 (credentials.json / token.json)."""
    from analise import gmail_api
    print("\n>>> Enviando via Gmail API (OAuth)...")
    id_mensagem = gmail_api.enviar_email(
        remetente=remetente,
        destinatario=destinatario,
        assunto=assunto,
        corpo=corpo,
        anexos=[caminho_zip],
    )
    print(f"✅ E-mail enviado com sucesso via OAuth! ID: {id_mensagem}")
    return True


def _enviar_via_smtp(remetente, destinatario, assunto, corpo, caminho_zip, senha):
    """Usa SMTP direto com uma Senha de Aplicativo do Gmail."""
    print("\n>>> Enviando via SMTP (Senha de Aplicativo)...")
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    with open(caminho_zip, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='zip', filename=os.path.basename(caminho_zip))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha)
            smtp.send_message(msg)
        print("✅ E-mail enviado com sucesso via SMTP!")
        return True
    except smtplib.SMTPAuthenticationError:
        raise Exception("Autenticação falhou! Verifique se você usou uma Senha de Aplicativo do Gmail (e não a senha normal da conta).")
    except Exception as e:
        raise Exception(f"Erro ao enviar via SMTP: {e}")


def enviar_relatorio_email(rodar_pipeline_antes=True):
    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    senha = os.getenv("EMAIL_SENHA")
    usar_oauth = _CREDENTIALS_JSON.exists()

    faltando = []
    if not remetente: faltando.append("EMAIL_REMETENTE")
    if not destinatario: faltando.append("EMAIL_DESTINATARIO")
    if not usar_oauth and not senha:
        faltando.append("EMAIL_SENHA (senha de aplicativo gerada no Gmail) — ou coloque credentials.json/token.json pra usar OAuth")

    if faltando:
        msg = "Faltam variáveis/arquivos: " + ", ".join(faltando)
        print(f"\n❌ {msg}")
        raise Exception(msg)

    if rodar_pipeline_antes:
        from main_analise import rodar_pipeline_completo
        rodar_pipeline_completo()

    caminho_zip, arquivos_incluidos = _compactar_relatorio()
    if caminho_zip is None:
        raise Exception("Nenhum CSV ou PNG encontrado. Rode a análise primeiro.")

    assunto = f"LuxeVoyage — Relatório de Análise ({datetime.now().strftime('%d/%m/%Y')})"
    corpo = "Olá,\n\nSegue em anexo o relatório de análise (CSVs + Gráficos)."

    if usar_oauth:
        return _enviar_via_oauth(remetente, destinatario, assunto, corpo, caminho_zip)
    return _enviar_via_smtp(remetente, destinatario, assunto, corpo, caminho_zip, senha)


if __name__ == "__main__":
    enviar_relatorio_email()

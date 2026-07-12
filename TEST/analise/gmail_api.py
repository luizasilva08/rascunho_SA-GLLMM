"""
analise/gmail_api.py — envio de e-mail usando a API oficial do Gmail (OAuth 2.0),
em vez de SMTP com senha. Baseado no fluxo "Aplicativo de desktop" do Google
Cloud Console.

Pré-requisitos (fazer uma vez só, no Google Cloud Console):
    1. Criar um projeto em https://console.cloud.google.com
    2. Ativar a "Gmail API" (APIs e Serviços > Biblioteca)
    3. Configurar a Tela de Consentimento OAuth (tipo Externo), e em
       "Usuários de teste" adicionar o e-mail que vai enviar as mensagens
    4. Em Credenciais > Criar Credenciais > ID do cliente OAuth
       > Tipo "Aplicativo de desktop"
    5. Baixar o JSON gerado, renomear para "credentials.json" e colocar
       na pasta CRUD-ANALISE/ (mesma pasta do main.py)

Na primeira execução, uma aba do navegador abre pedindo login/permissão.
Depois disso, um "token.json" é criado automaticamente e as próximas
execuções não pedem login de novo (o token é reaproveitado/renovado).

IMPORTANTE: nem credentials.json nem token.json devem ir pro Git — os
dois já foram adicionados ao .gitignore do projeto.
"""
import base64
import os
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopo mínimo necessário: só permissão para enviar e-mails (não lê nada).
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_ATUAL)  # TEST/


def _resolver_caminho(nome_arquivo):
    """
    Procura o arquivo em dois lugares, nessa ordem:
    1. TEST/<nome_arquivo>       -> uso local (rodando na sua máquina)
    2. /etc/secrets/<nome_arquivo> -> Secret Files do Render (produção)
    Retorna o primeiro caminho que existir; se nenhum existir, devolve o
    caminho local mesmo (pra manter a mensagem de erro original e útil).
    """
    caminho_local = os.path.join(PASTA_PROJETO, nome_arquivo)
    caminho_render = os.path.join("/etc/secrets", nome_arquivo)
    if os.path.exists(caminho_local):
        return caminho_local
    if os.path.exists(caminho_render):
        return caminho_render
    return caminho_local


CAMINHO_CREDENTIALS = _resolver_caminho("credentials.json")
CAMINHO_TOKEN = _resolver_caminho("token.json")


def obter_credenciais():
    """Faz login (na primeira vez) e devolve credenciais válidas, renovando
    o token automaticamente quando necessário."""
    creds = None
    if os.path.exists(CAMINHO_TOKEN):
        creds = Credentials.from_authorized_user_file(CAMINHO_TOKEN, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CAMINHO_CREDENTIALS):
                raise FileNotFoundError(
                    "credentials.json não encontrado em "
                    f"'{CAMINHO_CREDENTIALS}'. Baixe-o no Google Cloud Console "
                    "(Credenciais > ID do cliente OAuth > Aplicativo de desktop) "
                    "e coloque nessa pasta."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CAMINHO_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)

        try:
            with open(CAMINHO_TOKEN, "w") as token:
                token.write(creds.to_json())
        except OSError:
            # CAMINHO_TOKEN pode estar em /etc/secrets (Render), que é
            # somente-leitura. Sem problema: o refresh_token continua
            # válido e o token é renovado de novo na próxima chamada.
            pass

    return creds


def enviar_email(remetente, destinatario, assunto, corpo, anexos=None):
    """
    Envia um e-mail pela API do Gmail, com anexos opcionais.

    remetente: e-mail de quem está enviando (precisa ser o mesmo que fez
               login no fluxo OAuth / que está em "Usuários de teste")
    destinatario: e-mail de quem vai receber
    assunto: assunto do e-mail
    corpo: texto do e-mail (simples, sem HTML)
    anexos: lista de caminhos de arquivo para anexar (opcional)
    """
    creds = obter_credenciais()
    service = build("gmail", "v1", credentials=creds)

    if anexos:
        mensagem = MIMEMultipart()
        mensagem["Subject"] = assunto
        mensagem["From"] = remetente
        mensagem["To"] = destinatario
        mensagem.attach(MIMEText(corpo))

        for caminho in anexos:
            with open(caminho, "rb") as f:
                parte = MIMEApplication(f.read(), Name=os.path.basename(caminho))
            parte["Content-Disposition"] = f'attachment; filename="{os.path.basename(caminho)}"'
            mensagem.attach(parte)
    else:
        mensagem = EmailMessage()
        mensagem["Subject"] = assunto
        mensagem["From"] = remetente
        mensagem["To"] = destinatario
        mensagem.set_content(corpo)

    mensagem_encriptada = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()
    corpo_da_requisicao = {"raw": mensagem_encriptada}

    try:
        envio = service.users().messages().send(userId="me", body=corpo_da_requisicao).execute()
        return envio["id"]
    except HttpError as erro:
        raise RuntimeError(f"Erro na API do Gmail: {erro}") from erro

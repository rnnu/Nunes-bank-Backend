#email_service.py
import os
import requests

class ServicoEmail:
    """Encapsula o envio de e-mails de confirmação via API do Resend."""

    URL = "https://api.resend.com/emails"
    EMAIL_REMETENTE = "onboarding@resend.dev"

    def __init__(self, api_key=None):
        # A API key não fica escrita no código: vem da variável de ambiente.
        self.api_key = api_key or os.environ.get("RESEND_API_KEY", "")

    def enviar_codigo(self, email, codigo_ativacao):
        if not self.api_key:
            print("Erro: a variável de ambiente RESEND_API_KEY não está definida.")
            return False

        resposta = requests.post(
            self.URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": self.EMAIL_REMETENTE,
                "to": [email],
                "subject": "Confirmação de Email - Banco Nunes",
                "text": f"Seu código de ativação é: {codigo_ativacao}",
            },
        )

        if resposta.status_code >= 400:
            print(f"Erro ao enviar email: {resposta.status_code} - {resposta.text}")
            return False
        return True
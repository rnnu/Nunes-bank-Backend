#---------------utils.py----------------------

import hashlib
import random

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def erro_senha_fraca(senha):
    """Retorna uma mensagem de erro se a senha for fraca, ou None se for forte."""
    if len(senha) < 8:
        return "Senha fraca! A senha deve ter no mínimo 8 caracteres."
    if not any(c.isupper() for c in senha):
        return "Senha fraca! A senha deve conter pelo menos uma letra maiúscula."
    if not any(c.islower() for c in senha):
        return "Senha fraca! A senha deve conter pelo menos uma letra minúscula."
    if not any(c.isdigit() for c in senha):
        return "Senha fraca! A senha deve conter pelo menos um número."
    if not any(c in "!@#$%^&*()-+" for c in senha):
        return "Senha fraca! A senha deve conter pelo menos um caractere especial."
    return None


def gerar_codigo():
    return str(random.randint(100000, 999999))


class SaldoInsuficienteError(Exception):
    pass


class ValorInvalidoError(Exception):
    pass
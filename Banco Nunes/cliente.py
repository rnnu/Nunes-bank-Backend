#cliente.py
from utils import hash_senha

class Cliente:
    """Representa uma conta bancária: dados pessoais, saldo e extrato."""

    def __init__(
    self,
    id,
    nome,
    email,
    senha_hash,
    saldo=0.0,
):
        self.nome = nome
        self.email = email
        self.id = id
        self.senha_hash = senha_hash
        self.saldo = saldo

    def verificar_senha(self, senha):
        return self.senha_hash == hash_senha(senha)

    def redefinir_senha(self, nova_senha):
        self.senha_hash = hash_senha(nova_senha)

    def __str__(self):
        return f"Nome: {self.nome}, Email: {self.email}, Saldo: R${self.saldo:.2f}"
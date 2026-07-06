#transacao.py
import psycopg2
from datetime import datetime
class Transacao:
    """Um único lançamento no extrato (depósito ou saque)."""

    def __init__(self, tipo, valor, data=None):
        self.tipo = tipo
        self.valor = valor
        self.data = data or datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        sinal = "+" if self.tipo == "Depósito" else "-"
        return f"[{self.data}] {self.tipo}: {sinal}R${self.valor:.2f}"

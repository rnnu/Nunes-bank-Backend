#banco.py
import os
import re
import time
from database import Database
from cliente import Cliente
from exceptions import ValorInvalidoError,SaldoInsuficienteError
from email_service  import ServicoEmail
from utils import hash_senha,erro_senha_fraca, gerar_codigo
from decimal import Decimal
class Banco:
    """Gerencia a lista de usuários, persistência em banco de dados, cadastaro e login."""
    def __init__(self):
        self.database = Database()
        self.database.connect()
        self.servico_email = ServicoEmail()
    # ----------métodos de busca ----------
    def buscar_usuario_por_nome(self, nome):
        return self.database.buscar_cliente_por_nome(nome)
    
    def buscar_usuario_por_email(self, email):
        return self.database.buscar_cliente_por_email(email)
    
    # ---------- cadastro / login (fluxo interativo) ----------

    def criar_conta_interativo(self):
        email = input("Digite seu email: ").strip().lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Email inválido!")
            return

        if self.database.buscar_cliente_por_email(email):
            print("Email já cadastrado!")
            return

        codigo_ativacao = gerar_codigo()
        if not self.servico_email.enviar_codigo(email, codigo_ativacao):
            print("Não foi possível enviar o email de confirmação. Tente novamente mais tarde.")
            return

        codigo_usuario = input("Digite o código de ativação enviado para seu email: ")
        if codigo_usuario != codigo_ativacao:
            print("Código de ativação incorreto!")
            return

        print("Email confirmado com sucesso!")
        time.sleep(1)

        nome = input("Digite seu nome: ")
        if self.buscar_usuario_por_nome(nome):
            print("Nome de usuário já existe!")
            return

        while True:
            senha = input("Digite sua senha: ")
            erro = erro_senha_fraca(senha)
            if erro:
                print(erro)
                continue
            senha_hash = hash_senha(senha)
            if self.database.cadastrar_cliente(nome, email, senha_hash):
                print("Conta criada com sucesso!")
                break
            else:
                print("Erro ao criar conta. Tente novamente.")


    def redefinir_senha_interativo(self, usuario):
        print("Senha incorreta! Você precisa redefinir sua senha.")
        while True:
            nova_senha = input("Digite sua nova senha: ")
            erro = erro_senha_fraca(nova_senha)
            if erro:
                print(erro)
                continue
            nova_senha_hash = hash_senha(nova_senha)
            self.database.redefinir_senha_cliente(usuario.email, nova_senha_hash)  # Assuming email is the 3rd column in the database result
            print("Senha redefinida com sucesso!")
            break

    def login_interativo(self):
        email_login = input("Digite seu email: ").strip().lower()
        senha_login = input("Digite sua senha: ")

        cliente = self.database.buscar_cliente_por_email(email_login)
        if cliente is None:
            print("Email ou senha incorretos!")
            return
        if hash_senha(senha_login) != cliente.senha_hash:
            self.redefinir_senha_interativo(cliente)
            return
        print("Login realizado com sucesso!")
        self.menu_conta(cliente)

    # ---------- menu pós-login ----------

    def menu_conta(self, cliente):
        print("Carregando...")
        time.sleep(1)
        print(f"Bem-vindo, {cliente.nome}!")

        while True:
            print('-------------------------------------')
            print("Escolha uma opção:")
            print("1 - Consultar saldo")
            print("2 - Depositar")
            print("3 - Sacar")
            print("4 - Ver extrato")
            print("5 - Sair")
            print('-------------------------------------')
            opcao = input("Digite o número da opção desejada: ")

            if opcao == "1":
                # Consultar saldo com base no banco de dados
                cliente = self.database.buscar_cliente_por_email(cliente.email)  # Assuming email is the 3rd column in the database result
                if cliente is None:
                    print("Erro ao consultar saldo. Cliente não encontrado.")
                else:
                    print(f"Seu saldo é: R${cliente.saldo:.2f}")

            elif opcao == "2":
                try:
                    valor = Decimal(input("Digite o valor a ser depositado: "))
                    if  valor <= 0:
                        raise ValorInvalidoError("O valor do depósito deve ser maior que zero.")
                    saldo = self.database.buscar_saldo_cliente(cliente.email)
                    self.database.atualizar_saldo_cliente(cliente.email, saldo + valor)
                    cliente.saldo += valor  # Atualiza o saldo do cliente localmente
                    self.database.registrar_transacao( cliente.email, "depósito", valor)
                    print(f"Depósito de R${valor:.2f} realizado com sucesso!")
                except (ValorInvalidoError, ValueError) as e:
                    print(f"Valor inválido! {e}")

            elif opcao == "3":
                try:
                    valor = Decimal(input("Digite o valor a ser sacado: "))
                    if  valor <= 0:
                        raise ValorInvalidoError("O valor do saque deve ser maior que zero.")
                    saldo = self.database.buscar_saldo_cliente(cliente.email)
                    if saldo is None:
                        print("Erro ao consultar saldo. Cliente não encontrado.")
                    if saldo >= valor:
                        self.database.atualizar_saldo_cliente(cliente.email, saldo - valor)
                        cliente.saldo -= valor  # Atualiza o saldo do cliente localmente
                        self.database.registrar_transacao(cliente.email, "saque", valor)
                        print(f"Saque de R${valor:.2f} realizado com sucesso!")
                    else:
                        print("Saldo insuficiente!")
                except (ValorInvalidoError, ValueError) as e:
                    print(f"{e}")

            elif opcao == "4":
                extrato = self.database.buscar_extrato_cliente(cliente.email)  # Assuming email is the 3rd column in the database result    
                print("Seu extrato:")
                print('-------------------------------------')
                if not extrato:
                    print("Nenhuma transação registrada ainda.")
                else:
                    for t in extrato:
                        print(t)
                print('-------------------------------------')

            elif opcao == "5":
                break
            else:
                print("Opção inválida!")


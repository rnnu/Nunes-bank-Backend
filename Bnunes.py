import time
import json
import re
import hashlib
import random
import requests
 
ARQUIVO_USUARIOS = "usuarios.json"
 
# TODO: coloque aqui sua API key do Resend (https://resend.com/api-keys)
RESEND_API_KEY = "re_78kk5kEV_3uEgf4EHNbFPvt8DpyWRDTup"
# Enquanto não verificar um domínio próprio no Resend, o e-mail remetente
# precisa ser "onboarding@resend.dev" e só é possível enviar para o
# endereço com o qual você criou a conta no Resend.
EMAIL_REMETENTE = "onboarding@resend.dev"
 
 
def enviar_email_confirmacao(email, codigo_ativacao):
    resposta = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": EMAIL_REMETENTE,
            "to": [email],
            "subject": "Confirmação de Email - Banco Nunes",
            "text": f"Seu código de ativação é: {codigo_ativacao}",
        },
    )
 
    if resposta.status_code >= 400:
        print(f"Erro ao enviar email: {resposta.status_code} - {resposta.text}")
        return False
    return True
 
 
def gerar_codigo():
    return str(random.randint(100000, 999999))
 
 
def carregar_usuarios():
    try:
        with open(ARQUIVO_USUARIOS, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
 
 
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)
 
 
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
 
 
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()
 
 
def criar_conta(usuarios):
    email = input("Digite seu email: ")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Email inválido!")
        return
 
    if any(conta["email"] == email for conta in usuarios):
        print("Email já cadastrado!")
        return
 
    codigo_ativacao = gerar_codigo()
    if not enviar_email_confirmacao(email, codigo_ativacao):
        print("Não foi possível enviar o email de confirmação. Tente novamente mais tarde.")
        return
 
    codigo_usuario = input("Digite o código de ativação enviado para seu email: ")
    if codigo_usuario != codigo_ativacao:
        print("Código de ativação incorreto!")
        return
 
    print("Email confirmado com sucesso!")
    time.sleep(1)
 
    nome = input("Digite seu nome: ")
    if any(conta["nome"] == nome for conta in usuarios):
        print("Nome de usuário já existe!")
        return
 
    while True:
        senha = input("Digite sua senha: ")
        erro = erro_senha_fraca(senha)
        if erro:
            print(erro)
            continue
 
        conta = {
            "nome": nome,
            "email": email,
            "senha": hash_senha(senha),
            "saldo": 0,
        }
        usuarios.append(conta)
        salvar_usuarios(usuarios)
        print("Conta criada com sucesso!")
        break
 
 
def redefinir_senha(usuarios, conta):
    print("Senha incorreta! Deseja redefinir sua senha? (s/n)")
    resposta = input()
    if resposta.lower() != "s":
        return
 
    codigo_ativacao = gerar_codigo()
    if not enviar_email_confirmacao(conta["email"], codigo_ativacao):
        print("Não foi possível enviar o email de confirmação. Tente novamente mais tarde.")
        return
 
    codigo_usuario = input("Digite o código de ativação enviado para seu email: ")
    if codigo_usuario != codigo_ativacao:
        print("Código de ativação incorreto!")
        return
 
    nova_senha = input("Digite sua nova senha: ")
    erro = erro_senha_fraca(nova_senha)
    if erro:
        print(erro)
        return
 
    conta["senha"] = hash_senha(nova_senha)
    salvar_usuarios(usuarios)
    print("Senha redefinida com sucesso! Faça login novamente.")
 
 
def menu_conta(usuarios, conta):
    print("Carregando...")
    time.sleep(1)
    print(f"Bem-vindo de volta, {conta['nome']}!")
 
    while True:
        print('-------------------------------------')
        print("Escolha uma opção:")
        print("1 - Consultar saldo")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Sair")
        print('-------------------------------------')
        opcao2 = input("Digite o número da opção desejada: ")
 
        if opcao2 == "1":
            print(f"Seu saldo é: R${conta['saldo']:.2f}")
 
        elif opcao2 == "2":
            valor = float(input("Digite o valor a ser depositado: "))
            if valor <= 0:
                print("Valor inválido! O valor deve ser maior que zero.")
                continue
            conta["saldo"] += valor
            salvar_usuarios(usuarios)
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
 
        elif opcao2 == "3":
            valor = float(input("Digite o valor a ser sacado: "))
            if valor <= 0:
                print("Valor inválido! O valor deve ser maior que zero.")
                continue
            if valor > conta["saldo"]:
                print("Saldo insuficiente!")
                continue
            conta["saldo"] -= valor
            salvar_usuarios(usuarios)
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
 
        elif opcao2 == "4":
            break
        else:
            print("Opção inválida!")
 
 
def login(usuarios):
    email_login = input("Digite seu email: ")
    senha_login = input("Digite sua senha: ")
 
    conta = next((c for c in usuarios if c["email"] == email_login), None)
    if conta is None:
        print("Email ou senha incorretos!")
        return
 
    if conta["senha"] != hash_senha(senha_login):
        redefinir_senha(usuarios, conta)
        return
 
    print("Login realizado com sucesso!")
    menu_conta(usuarios, conta)
 
 
def main():
    usuarios = carregar_usuarios()
 
    print("Carregando...")
    time.sleep(1)
    print("Bem-vindo ao Banco Nunes!")
    time.sleep(1)
 
    while True:
        print("\nEscolha uma opção:")
        print("1 - Criar conta")
        print("2 - Login")
        print("3 - Sair")
        opcao = input("Digite o número da opção desejada: ")
 
        if opcao == "1":
            criar_conta(usuarios)
        elif opcao == "2":
            login(usuarios)
        elif opcao == "3":
            print('-------------------------------------')
            print("Saindo do Banco Nunes...")
            print('-------------------------------------')
            time.sleep(1)
            break
        else:
            print("Opção inválida!")
 
 
if __name__ == "__main__":
    main()
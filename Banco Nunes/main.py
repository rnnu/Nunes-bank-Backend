#-------------- main.py -------------
from banco import Banco
import time


def main():
    banco = Banco()

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
            banco.criar_conta_interativo()
        elif opcao == "2":
            banco.login_interativo()
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
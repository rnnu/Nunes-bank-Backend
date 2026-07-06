# 🏦 Banco Nunes

Sistema bancário desenvolvido em Python com persistência de dados em PostgreSQL.

## 📖 Sobre o projeto

O Banco Nunes é uma aplicação de terminal que simula as principais operações de um banco digital. O projeto foi desenvolvido para praticar Programação Orientada a Objetos (POO), integração com banco de dados, autenticação de usuários e consumo de APIs.

## ✨ Funcionalidades

- ✅ Cadastro de clientes
- ✅ Login de usuários
- ✅ Criptografia de senhas
- ✅ Confirmação de e-mail utilizando a API Resend
- ✅ Consulta de saldo
- ✅ Depósito
- ✅ Saque
- ✅ Extrato de transações
- ✅ Persistência de dados com PostgreSQL
- ✅ Tratamento de exceções personalizadas

## 🛠️ Tecnologias

- Python 3.14
- PostgreSQL
- psycopg2
- python-dotenv
- Resend API
- Git
- GitHub

## 📂 Estrutura do projeto

```
Banco Nunes/
│
├── main.py
├── banco.py
├── cliente.py
├── database.py
├── email_service.py
├── exceptions.py
├── transacao.py
├── utils.py
├── scripts/
│   └── criar_banco.py
├── .gitignore
└── README.md
```

## 🚀 Como executar

1. Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/Banco-Nunes.git
```

2. Entre na pasta do projeto:

```bash
cd Banco-Nunes
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banco_nunes
DB_USER=postgres
DB_PASSWORD=sua_senha

RESEND_API_KEY=sua_chave_da_resend
```

5. Crie as tabelas:

```bash
python scripts/criar_banco.py
```

6. Execute a aplicação:

```bash
python main.py
```

## 📌 Melhorias futuras

- Transferências entre contas
- Interface gráfica
- API REST
- Dashboard Web
- Autenticação em dois fatores (2FA)
- Testes automatizados
- Docker

## 👨‍💻 Autor

**Rafael Nunes Silva Carneiro**

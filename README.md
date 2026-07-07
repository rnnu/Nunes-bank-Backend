# 🏦 Banco Nunes

A digital banking system developed in Python with PostgreSQL data persistence.

## 📖 About the Project

Banco Nunes is a terminal-based banking application that simulates core digital banking operations.

The project was created to practice **Object-Oriented Programming (OOP)**, database integration, user authentication, secure password handling, and external API integration.

The application follows a modular architecture, separating business logic, database operations, services, and exceptions.

## ✨ Features

* ✅ Customer registration
* ✅ User authentication system
* ✅ Secure password hashing
* ✅ Email verification using Resend API
* ✅ Balance consultation
* ✅ Deposits
* ✅ Withdrawals
* ✅ Transaction history
* ✅ PostgreSQL database persistence
* ✅ Custom exception handling

## 🛠️ Technologies

* Python
* PostgreSQL
* psycopg2
* python-dotenv
* Resend API
* Git
* GitHub

## 🏗️ Project Architecture

```
Banco Nunes/
│
├── main.py              # Application entry point
├── banco.py             # Banking business logic
├── cliente.py           # Customer entity
├── database.py          # Database connection and queries
├── email_service.py     # Email verification service
├── exceptions.py        # Custom exceptions
├── transacao.py         # Transaction management
├── utils.py             # Utility functions
│
├── scripts/
│   └── criar_banco.py   # Database setup script
│
├── .gitignore
└── README.md
```

## 🚀 Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/SEU-USUARIO/Banco-Nunes.git
```

### 2. Navigate to the project folder

```bash
cd Banco-Nunes
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banco_nunes
DB_USER=postgres
DB_PASSWORD=your_password

RESEND_API_KEY=your_resend_api_key
```

### 5. Create the database tables

```bash
python scripts/criar_banco.py
```

### 6. Run the application

```bash
python main.py
```

## 🔮 Future Improvements

* Bank transfers between accounts
* Graphical user interface
* REST API integration
* Web dashboard
* Two-factor authentication (2FA)
* Automated testing
* Docker containerization

## 👨‍💻 Author

**Rafael Nunes Silva Carneiro**

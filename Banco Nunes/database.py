#Database.py
import psycopg2
from cliente import Cliente
from dotenv import load_dotenv
import os


load_dotenv()


class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", 5432))

        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
         host=self.host,
         database=self.database,
        user=self.user,
        password=self.password,
        port=self.port
    )
    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if self.connection is None  or self.connection.closed:
                self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(query,params)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"erro ao executar a consulta :{e}")
        


    def fetch_query(self, query, params=None):
        try:
            if self.connection is None or self.connection.closed:
                self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
    
    def cadastrar_cliente(self, nome, email, senha_hash):
        if self.buscar_cliente_por_email(email):
            print("Cliente já cadastrado no banco de dados.")
            return False
        query = "INSERT INTO clientes (nome, email, senha_hash, saldo) VALUES (%s, %s, %s, %s)"
        self.execute_query(query, (nome, email, senha_hash, 0.00))
        print("Cliente cadastrado com sucesso.")
        return True
    
    def buscar_cliente_por_email(self, email):
        query = "SELECT * FROM clientes WHERE email = %s"
        result = self.fetch_query(query, (email,))
        if not result:
            return None
        id, nome, email, senha_hash, saldo = result[0]
        cliente= Cliente(id, nome, email, senha_hash, saldo)
        return cliente

    
    def atualizar_saldo_cliente(self, email, novo_saldo):
        query = "UPDATE clientes SET saldo = %s WHERE email = %s"
        self.execute_query(query, (novo_saldo, email))
        print("Saldo do cliente atualizado com sucesso.")
    
    def buscar_saldo_cliente(self, email):
        query = "SELECT saldo FROM clientes WHERE email = %s"
        result = self.fetch_query(query, (email,))
        return result[0][0] if result else None
    
    def registrar_transacao(self, email, tipo, valor):
        query = "INSERT INTO transacoes (email_cliente, tipo, valor) VALUES (%s, %s, %s)"
        self.execute_query(query, (email, tipo, valor))
    
    def buscar_extrato_cliente(self, email):
        query = "SELECT * FROM transacoes WHERE email_cliente = %s ORDER BY data DESC"
        return self.fetch_query(query, (email,))
    
    def redefinir_senha_cliente(self, email, nova_senha_hash):
        query = "UPDATE clientes SET senha_hash = %s WHERE email = %s"
        self.execute_query(query, (nova_senha_hash, email))
        print("Senha do cliente redefinida com sucesso.")

    def buscar_cliente_por_id(self, cliente_id):
        query = "SELECT * FROM clientes WHERE id = %s"
        result = self.fetch_query(query, (cliente_id,))
        if not result:
            return None
        id, nome, email, senha_hash, saldo = result[0]
        return Cliente(id, nome, email, senha_hash, saldo)
    
    def buscar_cliente_por_nome(self, nome):
        query = "SELECT * FROM clientes WHERE nome = %s"
        result = self.fetch_query(query, (nome,))
        if not result:
            return None
        id, nome, email, senha_hash, saldo = result[0]
        return Cliente(id, nome, email, senha_hash, saldo)          



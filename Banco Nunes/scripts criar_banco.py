#aqui vamos importar as bibliotecas necessárias para a conexão com o banco de dados e para a manipulação de dados.
import email
import datetime
import psycopg2
#aqui vamos criar uma instância da classe Database, que será responsável por gerenciar a conexão com o banco de dados e realizar operações de CRUD (Create, Read, Update, Delete) nos dados dos clientes.


class Database:
    def __init__(self, host="localhost", database="banco_nunes", user="postgres", password="1818"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None  
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")
    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                print("Consulta executada com sucesso.")
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")

db = Database()
db.connect()

db.execute_query("""CREATE TABLE IF NOT EXISTS clientes 
                 (id SERIAL PRIMARY KEY, 
                 nome VARCHAR(100), 
                 email VARCHAR(100), 
                 senha_hash VARCHAR(255),
                 saldo DECIMAL(10, 2) DEFAULT 0.00
                 )""")
#criar tabela para transações
db.execute_query("""CREATE TABLE IF NOT EXISTS transacoes
                    (id SERIAL PRIMARY KEY,
                     email_cliente VARCHAR(100),
                     tipo VARCHAR(50),
                     valor DECIMAL(10, 2),
                     data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")

db.close()
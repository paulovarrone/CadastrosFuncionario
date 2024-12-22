import mysql.connector


def connection():
    conexao = mysql.connector.connect(
        host = 'localhost', #para docker host.docker.internal
        user = 'root',
        password = '',
        database = 'recursos_humanos'
    )

    return conexao

def criar_banco():
    conexao = mysql.connector.connect(
        host='localhost', #para docker host.docker.internal
        user='root',
        password=''
    )
    cursor = conexao.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS recursos_humanos')
    conexao.commit()
    conexao.close()

def criar_funcionario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionario(
            id INT AUTO_INCREMENT UNIQUE,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(10) PRIMARY KEY,
            nascimento DATE NOT NULL,
            contratacao DATE NOT NULL,
            status VARCHAR(10) NOT NULL,
            updated_by VARCHAR(50) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            foto LONGTEXT NOT NULL,
            assinatura LONGTEXT NOT NULL
        ) 
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_usuario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario (
            id INT AUTO_INCREMENT UNIQUE,
            email VARCHAR(50) NOT NULL UNIQUE,
            username VARCHAR(50) NOT NULL PRIMARY KEY,
            password VARCHAR(250) NOT NULL,
            cpf VARCHAR(250) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()
    conexao.close()
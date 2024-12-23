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
            usuario_cadastrante VARCHAR(50) NOT NULL,
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

def usuario_logado():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario_logado (
            id INT AUTO_INCREMENT UNIQUE,
            email VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            hora_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()

def usuario_deslogado():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario_deslogado (
            id INT AUTO_INCREMENT UNIQUE,
            email VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            hora_saida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()

def usuario_alterou_dados_func():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario_alterou_dados_func (
            id INT AUTO_INCREMENT UNIQUE,
            email_user_alterou VARCHAR(50) NOT NULL,
            username_user_alterou VARCHAR(50) NOT NULL,
            nome_funcionario VARCHAR(50) NOT NULL,
            matricula_funcionario VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT NULL, 
            foto VARCHAR(50) DEFAULT NULL,
            assinatura VARCHAR(50) DEFAULT NULL,             
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()

def usuario_select_funcionario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario_select_funcionario (
            id INT AUTO_INCREMENT UNIQUE,
            email VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL,
            nome_funcionario_selecionado VARCHAR(50) NOT NULL,
            matricula_funcionario_selecionado VARCHAR(50) NOT NULL,       
            hora_selecao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()

def usuario_cadastrou_funcionario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario_cadastrou_funcionario (
            id INT AUTO_INCREMENT UNIQUE,
            email_cadastrante VARCHAR(50) NOT NULL,
            username_cadastrante VARCHAR(50) NOT NULL,
            nome_funcionario VARCHAR(50) NOT NULL,
            matricula_funcionario VARCHAR(50) NOT NULL,       
            hora_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    cursor.close()

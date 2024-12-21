from app.controllers.banco import *
from flask import *
from app.extensions.bcrypt import bcrypt

def cadastrar_usuario(email, username, password, cpf):
    conexao = connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Verificar se o e-mail ou username já existe
        cursor.execute("SELECT * FROM usuario WHERE email = %s OR username = %s OR cpf = %s", (email, username, cpf))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            if usuario_existente['email'] == email:
                flash('E-mail já cadastrado!', 'erro')
                current_app.logger.warning(f"Tentativa de cadastro com e-mail existente: {email}")
            if usuario_existente['username'] == username:
                flash('Nome de usuário já cadastrado!', 'erro')
                current_app.logger.warning(f"Tentativa de cadastro com username existente: {username}")
            if usuario_existente['cpf'] == cpf:
                flash('CPF de usuário já cadastrado!', 'erro')
                current_app.logger.warning(f"Tentativa de cadastro com CPF existente: {cpf}")
            return False  # Retorna falso se o usuário já existir

        # Gerar hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        

        hashed_cpf = bcrypt.generate_password_hash(cpf).decode('utf-8')
        

        # Inserir novo usuário
        cursor.execute("INSERT INTO usuario (email, username, password, cpf) VALUES (%s, %s, %s, %s)", 
                       (email, username, hashed_password, hashed_cpf))
        conexao.commit()
        current_app.logger.info(f"Usuario {username} cadastrado com sucesso.")
        flash('Usuário cadastrado com sucesso.', 'sucesso')
        return True  # Retorna verdadeiro se o cadastro foi bem-sucedido
    except Exception as e:
        current_app.logger.error(f"Erro ao cadastrar o usuário: {e}")
        flash('Erro ao cadastrar o usuário.', 'erro')
        return False
    finally:
        cursor.close()
        conexao.close()
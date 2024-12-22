from app.controllers.banco import connection
from flask import current_app
from app.extensions.bcrypt import bcrypt


def autenticar_usuario(email,username, password):
    conexao = connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM usuario WHERE username = %s and email = %s", (username,email))
        user = cursor.fetchone()

        if user:
            if bcrypt.check_password_hash(user['password'], password):
                current_app.logger.info(f"Usuario {username} autenticado com sucesso.")
                return user
            else:
                current_app.logger.warning(f"Falha de login para o usuario {username} com E-mail {email}: senha incorreta.")
                current_app.logger.error("Senha incorreta!")
        else:
            current_app.logger.warning(f"Falha de login para o usuario {username}: usuario nao encontrado.")
            current_app.logger.error(f"Usuario {username} nao encontrado!")
    finally:
        cursor.close()
        conexao.close()

    return None
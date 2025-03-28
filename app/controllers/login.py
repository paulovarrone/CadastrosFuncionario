# from app.controllers.banco import *
from flask import render_template, request, redirect, url_for, session, flash, current_app
from app.controllers.autenticar_user import autenticar_usuario
from app.controllers.auditoria.usuario_logado.usuario_logado import auditoria_banco_login

def logar():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = autenticar_usuario(email,username, password)
        if user:
            session['user'] = user['username']  # Salva o usuário na sessão
            session['email']= user['email']
            current_app.logger.info(f"Usuario {username}, E-mail {email} logado com sucesso.")

            auditoria_banco_login(email, username)

            flash(f'Login realizado com sucesso. Bem-vindo {username}', 'sucesso')
            return redirect(url_for('index.index'))
        else:
            current_app.logger.warning(f"Tentativa de login falhada para o usuario {username}.")
            flash('Credenciais inválidas. Tente novamente.', 'erro')

    return render_template('login.html')
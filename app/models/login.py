from app.models.banco import *
from flask import *
from app.models.autenticar_user import autenticar_usuario


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
            flash(f'Login realizado com sucesso. Bem-vindo {username}', 'sucesso')
            return redirect(url_for('index.index'))
        else:
            current_app.logger.warning(f"Tentativa de login falhada para o usuario {username}.")
            flash('Credenciais inválidas. Tente novamente.', 'erro')

    return render_template('login.html')
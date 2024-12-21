from flask import *
from app.models.cadastrar_usuario import cadastrar_usuario

def registrar_usuario():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cpf = request.form['cpf']


        if password != confirm_password:
            flash('As senhas não coincidem!', 'erro')
        else:
            sucesso = cadastrar_usuario(email, username, password, cpf)
            if sucesso:
                return redirect(url_for('login.login'))
            else:
                return render_template('registrarUsuario.html', email=email, username=username)

    return render_template('registrarUsuario.html')
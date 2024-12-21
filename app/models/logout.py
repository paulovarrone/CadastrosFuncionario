from flask import *


def deslogar():
    username = session.get('user', None)
    email = session.get('email', None)
    session.pop('user', None)
    session.pop('email', None)
    current_app.logger.info(f"Usuario {username} {email} saiu do sistema.")
    flash('Você saiu do sistema.', 'sucesso')
    return redirect(url_for('login.login'))
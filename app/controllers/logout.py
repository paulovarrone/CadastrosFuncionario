from flask import session, redirect, url_for, flash, current_app
from app.controllers.auditoria.usuario_deslogado.usuario_deslogado import auditoria_banco_deslogado

def deslogar():
    username = session.get('user', None)
    email = session.get('email', None)
    session.pop('user', None)
    session.pop('email', None)

    auditoria_banco_deslogado(email, username)

    current_app.logger.info(f"Usuario {username} {email} saiu do sistema.")
    flash('Você saiu do sistema.', 'sucesso')
    return redirect(url_for('login.login'))
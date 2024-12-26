from datetime import datetime, timedelta
from flask import session, redirect, url_for,flash, current_app
from app.controllers.auditoria.usuario_deslogado.usuario_deslogado import auditoria_banco_deslogado

def timeout():

    timeout = timedelta(minutes=10)
    last_activity = session.get('last_activity', None)

    username = session.get('user', None)
    email = session.get('email', None)

    if last_activity:

        last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
        conta_tempo = datetime.now() - last_activity_time > timeout

        if conta_tempo:   
            session.clear()
            auditoria_banco_deslogado(email, username)
            flash("Sua sessão expirou por inatividade. Faça login novamente.", "erro")
            current_app.logger.info(f"Usuario {username} {email} levou timeout do sistema.")
            return redirect(url_for('login.login'))


    session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

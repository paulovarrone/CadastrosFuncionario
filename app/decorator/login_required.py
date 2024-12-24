from flask import redirect, session, url_for, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa estar logado para acessar essa página.', 'erro')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function
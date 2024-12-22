from flask import Blueprint
from app.controllers.login import logar

bp = Blueprint('login', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    return logar()

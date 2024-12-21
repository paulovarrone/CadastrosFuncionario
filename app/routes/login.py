from flask import *
from app.models.login import logar

bp = Blueprint('login', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    return logar()

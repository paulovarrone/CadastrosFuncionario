from flask import *
from app.decorator.login_required import login_required
from app.controllers.cadastro_funcionario import cadastro_funcinarios

bp = Blueprint('cadastroDeFuncionario', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def cadastroDeFuncionario():
    return cadastro_funcinarios()
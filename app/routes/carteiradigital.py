from flask import *
from app.controllers.selecionar_e_cadastrar import selecionar_para_cadastrar
from app.controllers.decorator.login_required import login_required

bp = Blueprint('carteiradigital', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def carteiradigital():
    return selecionar_para_cadastrar()
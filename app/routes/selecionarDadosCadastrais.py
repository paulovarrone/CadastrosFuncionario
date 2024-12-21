from flask import *
from app.models.selecionar_dados import selecionar_dados_cadastrais
from app.models.decorator.login_required import login_required

bp = Blueprint('selecionarDadosCadastrais', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def selecionarDadosCadastrais():
    return selecionar_dados_cadastrais()
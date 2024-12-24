from flask import render_template, request, Blueprint
from app.controllers.bi.bi import fetch_data_situacao, fetch_data_identificacao_sexual, situacao, identificacao_sexual
from app.decorator.login_required import login_required

bp = Blueprint('powerBI', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def powerBI():
    df_situacao = fetch_data_situacao()
    df_identificacao_sexual = fetch_data_identificacao_sexual()
    
    filtro = request.args.get('status', '')

    situacao_funcionario = situacao()
    identificacao_sexual_funcionario = identificacao_sexual()

    if filtro and filtro != 'Todos':
        df_situacao = df_situacao[df_situacao['status'] == filtro]


    return render_template(
                           'bi.html', tabela = df_situacao.to_dict(orient='records'), 
                           situacao_funcionario = situacao_funcionario, 
                           identificacao_sexual_funcionario = identificacao_sexual_funcionario, 
                           filtro = filtro
                        )
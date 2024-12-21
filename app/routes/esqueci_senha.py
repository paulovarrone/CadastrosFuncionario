from flask import *
from app.controllers.esqueci_senha import mudar_senha

bp = Blueprint('esqueci_senha', __name__)

@bp.route('/', methods=['GET','POST'])
def esqueci_senha():
    return mudar_senha()
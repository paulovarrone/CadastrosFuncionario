from flask import *
from app.models.registrar_usuario import registrar_usuario

bp = Blueprint('registrarUsuario', __name__)

@bp.route('/', methods=['GET', 'POST'])
def registrarUsuario():
    return registrar_usuario()
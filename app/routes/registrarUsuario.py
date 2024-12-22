from flask import Blueprint
from app.controllers.registrar_usuario import registrar_usuario

bp = Blueprint('registrarUsuario', __name__)

@bp.route('/', methods=['GET', 'POST'])
def registrarUsuario():
    return registrar_usuario()
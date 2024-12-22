from flask import Blueprint
from app.controllers.logout import deslogar

bp = Blueprint('logout', __name__)

@bp.route('/')
def logout():
    return deslogar()
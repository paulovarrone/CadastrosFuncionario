from flask import *
from app.controllers.decorator.login_required import login_required

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')
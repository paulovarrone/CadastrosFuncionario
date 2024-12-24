from flask import Flask
from dotenv import load_dotenv
import os
from app.extensions.bcrypt import bcrypt
from app.routes import index_bp, login_bp, cadastroDeFuncionario_bp, carteiradigital_bp, esqueci_senha_bp, logout_bp, registrarUsuario_bp, selecionarDadosCadastrais_bp, powerBI_bp
from app.middleware.timeout import timeout
from app.controllers.banco import banco
from app.controllers.logs_auditoria import setup_logging
import matplotlib

load_dotenv()
matplotlib.use('Agg')

def create_app():
   
    static_path = os.path.join('app','static', 'imgBI')

    # Verifica se o diretório existe e cria se necessário
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    bcrypt.init_app(app)

    app.before_request(timeout)
    banco()
    setup_logging(app)

    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(registrarUsuario_bp, url_prefix='/registrarUsuario')
    app.register_blueprint(cadastroDeFuncionario_bp, url_prefix='/cadastroDeFuncionario')
    app.register_blueprint(carteiradigital_bp, url_prefix='/carteiradigital')
    app.register_blueprint(esqueci_senha_bp, url_prefix='/esqueci_senha')
    app.register_blueprint(logout_bp, url_prefix='/logout')
    app.register_blueprint(selecionarDadosCadastrais_bp, url_prefix='/selecionarDadosCadastrais')
    app.register_blueprint(powerBI_bp, url_prefix='/powerBI')

    return app

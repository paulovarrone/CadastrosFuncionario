from flask import Flask
from dotenv import load_dotenv
import os
from app.extensions.bcrypt import bcrypt
from app.routes import index_bp, login_bp, cadastroDeFuncionario_bp, carteiradigital_bp, esqueci_senha_bp, logout_bp, registrarUsuario_bp, selecionarDadosCadastrais_bp
from app.middleware.timeout import timeout

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    bcrypt.init_app(app)

    app.before_request(timeout)

    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(registrarUsuario_bp, url_prefix='/registrarUsuario')
    app.register_blueprint(cadastroDeFuncionario_bp, url_prefix='/cadastroDeFuncionario')
    app.register_blueprint(carteiradigital_bp, url_prefix='/carteiradigital')
    app.register_blueprint(esqueci_senha_bp, url_prefix='/esqueci_senha')
    app.register_blueprint(logout_bp, url_prefix='/logout')
    app.register_blueprint(selecionarDadosCadastrais_bp, url_prefix='/selecionarDadosCadastrais')

    return app

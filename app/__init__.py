from flask import Flask
from dotenv import load_dotenv
import os
from app.routes import index, login, cadastroDeFuncionario, carteiradigital, esqueci_senha, logout, registrarUsuario, selecionarDadosCadastrais
from app.extensions.bcrypt import bcrypt


load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    bcrypt.init_app(app)

    app.register_blueprint(index.bp, url_prefix='/')
    app.register_blueprint(login.bp, url_prefix='/login')
    app.register_blueprint(registrarUsuario.bp, url_prefix='/registrarUsuario')
    app.register_blueprint(cadastroDeFuncionario.bp, url_prefix='/cadastroDeFuncionario')
    app.register_blueprint(carteiradigital.bp, url_prefix='/carteiradigital')
    app.register_blueprint(esqueci_senha.bp, url_prefix='/esqueci_senha')
    app.register_blueprint(logout.bp, url_prefix='/logout')
    app.register_blueprint(selecionarDadosCadastrais.bp, url_prefix='/selecionarDadosCadastrais')

    return app

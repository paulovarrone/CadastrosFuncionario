import mysql.connector
from mysql.connector.errors import IntegrityError
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
import os
from datetime import time, timedelta, datetime
import base64
from functools import wraps
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)

# logging.basicConfig(filename='infoLogs.log', level=logging.INFO,
#                     format='%(asctime)s:%(levelname)s:%(message)s')

def setup_logging():
    # Criar manipulador para INFO
    info_handler = RotatingFileHandler('infoLogs.log')
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Criar manipulador para WARNING
    warning_handler = RotatingFileHandler('warningLogs.log')
    warning_handler.setLevel(logging.WARNING)
    warning_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    warning_handler.setFormatter(warning_formatter)

    # Criar manipulador para ERROR
    error_handler = RotatingFileHandler('errorLogs.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)

    # Configurar o logger principal
    logger = logging.getLogger()
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    # Também pode configurar um manipulador de console, se necessário
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


def connection():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'recursos_humanos'
    )

    return conexao

def criar_banco():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    cursor = conexao.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS recursos_humanos')
    conexao.commit()
    conexao.close()

def criar_funcionario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionario(
            id INT AUTO_INCREMENT UNIQUE,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(10) PRIMARY KEY,
            nascimento DATE NOT NULL,
            contratacao DATE NOT NULL,
            status VARCHAR(10) NOT NULL,
            foto LONGTEXT NOT NULL,
            assinatura LONGTEXT NOT NULL
        ) 
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

def criar_usuario():
    conexao = connection()
    cursor = conexao.cursor()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS usuario (
            id INT AUTO_INCREMENT UNIQUE,
            email VARCHAR(50) NOT NULL UNIQUE,
            username VARCHAR(50) NOT NULL PRIMARY KEY,
            password VARCHAR(250) NOT NULL
        )
    ''')

    conexao.commit()
    cursor.close()
    conexao.close()

def cadastrar_usuario(email, username, password):
    conexao = connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Verificar se o e-mail ou username já existe
        cursor.execute("SELECT * FROM usuario WHERE email = %s OR username = %s", (email, username))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            if usuario_existente['email'] == email:
                flash('E-mail já cadastrado!', 'erro')
                app.logger.warning(f"Tentativa de cadastro com e-mail existente: {email}")
            if usuario_existente['username'] == username:
                flash('Nome de usuário já cadastrado!', 'erro')
                app.logger.warning(f"Tentativa de cadastro com username existente: {username}")
            return False  # Retorna falso se o usuário já existir

        # Gerar hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        app.logger.info(f"Hash gerado para {username}: {hashed_password}")

        # Inserir novo usuário
        cursor.execute("INSERT INTO usuario (email, username, password) VALUES (%s, %s, %s)", 
                       (email, username, hashed_password))
        conexao.commit()
        app.logger.info(f"Usuário {username} cadastrado com sucesso.")
        flash('Usuário cadastrado com sucesso.', 'sucesso')
        return True  # Retorna verdadeiro se o cadastro foi bem-sucedido
    except Exception as e:
        app.logger.error(f"Erro ao cadastrar o usuário: {e}")
        flash('Erro ao cadastrar o usuário.', 'erro')
        return False
    finally:
        cursor.close()
        conexao.close()


def autenticar_usuario(email,username, password):
    conexao = connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM usuario WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            app.logger.info(f"Hash armazenado para {username}: {user['password']}")
            if bcrypt.check_password_hash(user['password'], password):
                app.logger.info(f"Usuario {username} autenticado com sucesso.")
                return user
            else:
                app.logger.warning(f"Falha de login para o usuario {username}: senha incorreta.")
                app.logger.error("Senha incorreta!")
        else:
            app.logger.warning(f"Falha de login para o usuario {username}: usuario nao encontrado.")
            app.logger.error(f"Usuario {username} nao encontrado!")
    finally:
        cursor.close()
        conexao.close()

    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem!', 'erro')
        else:
            sucesso = cadastrar_usuario(email, username, password)
            if sucesso:
                return redirect(url_for('login'))
            else:
                return render_template('register.html', email=email, username=username)

    return render_template('register.html')


# Rotas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = autenticar_usuario(email,username, password)
        if user:
            session['user'] = user['username']  # Salva o usuário na sessão
            app.logger.info(f"Usuario {username} logado com sucesso.")
            flash('Login realizado com sucesso.', 'sucesso')
            return redirect(url_for('index'))
        else:
            app.logger.warning(f"Tentativa de login falhada para o usuario {username}.")
            flash('Credenciais inválidas. Tente novamente.', 'erro')

    return render_template('login.html')



# Decorador para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa estar logado para acessar essa página.', 'erro')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/logout')
def logout():
    username = session.get('user', None)
    session.pop('user', None)
    app.logger.info(f"Usuario {username} saiu do sistema.")
    flash('Você saiu do sistema.', 'sucesso')
    return redirect(url_for('login'))



@app.route('/')
@login_required
def index():
    return render_template('index.html')


    
def imagem_para_base64(imagem):
    if imagem:
        return base64.b64encode(imagem.read()).decode('utf-8')
    return None



@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_funcinario():

    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula'].strip()
        nascimento = request.form['nascimento']
        contratacao = request.form['contratacao']
        status = request.form['status']
        foto = request.files.get('foto')
        assinatura = request.files.get('assinatura')

        conexao = connection()
        cursor = conexao.cursor(dictionary=True)



        foto_b64 = imagem_para_base64(foto)
        assinatura_b64 = imagem_para_base64(assinatura)

        try:
            cursor.execute("SELECT * FROM funcionario WHERE matricula = %s", (matricula,))
            pessoa = cursor.fetchall()

            if not pessoa:
                query = ("INSERT INTO funcionario(nome,matricula,nascimento,contratacao,status,foto,assinatura) VALUES(%s,%s,%s,%s,%s,%s,%s)")
                valores = (nome,matricula,nascimento,contratacao,status,foto_b64,assinatura_b64)

                cursor.execute(query, valores)
                conexao.commit()
                app.logger.info(f"Usuario {session['user']} cadastrou o funcionario {nome} matricula {matricula}.")
                flash('Cadastro realizado com sucesso.', 'sucesso')
            else:
                if pessoa[0]['matricula'] == matricula:
                    app.logger.warning(f"Tentativa de cadastro com matricula {matricula} que ja existe.")
                    flash('Usuário já cadastrado com essa matricula.', 'erro')
        
        except IntegrityError as err:
            app.logger.error(f"Erro de integridade ao tentar cadastrar funcionario {matricula}: {err}")
            flash(f"Erro de integridade: {err}", 'erro')
        
        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('index'))

    
    return render_template('index.html')


    
# @app.route('/alterar', methods=['GET', 'POST'])
# def alterar_dados_cadastrais():
#     return render_template('alter.html')

@app.route('/selecionar', methods=['GET', 'POST'])
@login_required
def select_dados_cadastrais():
    pessoa = None

    if request.method == 'POST':
        matricula = request.form['matricula'].strip()
        
        try:
            conexao = connection()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute('SELECT * FROM funcionario WHERE matricula = %s', (matricula,))
            pessoa = cursor.fetchone()

            if not pessoa:
                flash('Usuário não encontrado no sistema.', 'erro')
            else:
                # Salva a matrícula na sessão
                session['matricula'] = matricula
                app.logger.info(f"Usuario {session['user']} selecionou dados do funcionario {pessoa['nome']} com matricula {matricula}")
        except Exception as e:
            flash(f"Erro {e}", 'erro')

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('select_dados_cadastrais'))

    # Recupera a matrícula da sessão e busca novamente os dados
    matricula = session.pop('matricula', None)
    if matricula:
        try:
            conexao = connection()
            cursor = conexao.cursor(dictionary=True)

            cursor.execute('SELECT * FROM funcionario WHERE matricula = %s', (matricula,))
            pessoa = cursor.fetchone()

            if pessoa:
                if pessoa.get('foto'):
                    pessoa['foto'] = f"data:image/jpeg;base64,{pessoa['foto']}"
                if pessoa.get('assinatura'):
                    pessoa['assinatura'] = f"data:image/jpeg;base64,{pessoa['assinatura']}"

        except Exception as e:
            flash(f"Erro {e}", 'erro')

        finally:
            cursor.close()
            conexao.close()

    return render_template('select.html', pessoa=pessoa)



@app.route('/carteiradigital', methods=['GET', 'POST'])
@login_required
def selecionar_e_cadastrar():
    pessoa = None
    if request.method == 'POST':
        matricula = request.form.get('matricula', '').strip()
        
        # Processo de seleção do funcionário
        if 'foto' not in request.files:
            try:
                conexao = connection()
                cursor = conexao.cursor(dictionary=True)
                cursor.execute('SELECT * FROM funcionario WHERE matricula = %s', (matricula,))
                pessoa = cursor.fetchone()
                
                if not pessoa:
                    app.logger.warning(f"Funcionario com matricula {matricula} nao encontrado para atualizaçao.")
                    flash('Usuário não encontrado no sistema.', 'erro')
                else:
                    app.logger.info(f"Usuario {session['user']} acessou os dados do funcionario {pessoa['nome']} com matricula {matricula}.")
            except Exception as e:
                app.logger.error(f'Erro ao buscar funcionario {matricula} para atualizaçao: {e}')
                flash(f'Erro ao buscar funcionário: {e}', 'erro')
            finally:
                cursor.close()
                conexao.close()
        else:
            # Processo de atualização de fotos e assinatura
            foto = request.files.get('foto')
            assinatura = request.files.get('assinatura')
            status = request.form['status']
            nome = request.form['nome']

            if not matricula:
                app.logger.warning('Matrícula não fornecida para atualização.')
                flash('Matrícula é obrigatória para atualizar fotos.', 'erro')
                return redirect(url_for('selecionar_e_cadastrar'))

            foto_b64 = imagem_para_base64(foto)
            assinatura_b64 = imagem_para_base64(assinatura)

            try:
                conexao = connection()
                cursor = conexao.cursor(dictionary=True)
                cursor.execute("SELECT * FROM funcionario WHERE matricula = %s", (matricula,))
                pessoa = cursor.fetchone()
                if pessoa:
                    query = "UPDATE funcionario SET foto = %s, assinatura = %s, status = %s WHERE matricula = %s"
                    cursor.execute(query, (foto_b64, assinatura_b64,status, matricula))
                    conexao.commit()
                    app.logger.info(f"Usuario {session['user']} atualizou os dados de {nome} com matricula {matricula} status {status}")
                    flash('Dados atualizadas com sucesso.', 'sucesso')
                    return redirect(url_for('selecionar_e_cadastrar'))
                else:
                    app.logger.warning(f"Funcionario com matricula {matricula} nao encontrado para atualizacao.")
                    flash('Usuário não encontrado para atualizar dados.', 'erro')
            except Exception as e:
                app.logger.error(f'Erro ao atualizar dados do funcionario {matricula}: {e}')
                flash(f'Erro ao atualizar dados: {e}', 'erro')
            finally:
                cursor.close()
                conexao.close()

      
    return render_template('carteira.html', pessoa=pessoa)


if __name__ == '__main__':
    criar_banco()
    criar_funcionario()
    criar_usuario()
    setup_logging()
    app.run(host='0.0.0.0', port=5003, debug=True)
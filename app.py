import mysql.connector
from mysql.connector.errors import IntegrityError
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
import os
from datetime import time, timedelta, datetime
import base64


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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


@app.route('/')
def index():
    return render_template('index.html')


    
def imagem_para_base64(imagem):
    if imagem:
        return base64.b64encode(imagem.read()).decode('utf-8')
    return None



@app.route('/cadastro', methods=['GET', 'POST'])
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
                flash('Cadastro realizado com sucesso.', 'sucesso')
            else:
                if pessoa[0]['matricula'] == matricula:
                    flash('Usuário já cadastrado com essa matricula.', 'erro')
        
        except IntegrityError as err:
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
                    flash('Usuário não encontrado no sistema.', 'erro')
            except Exception as e:
                flash(f'Erro ao buscar funcionário: {e}', 'erro')
            finally:
                cursor.close()
                conexao.close()
        else:
            # Processo de atualização de fotos e assinatura
            foto = request.files.get('foto')
            assinatura = request.files.get('assinatura')
            status = request.form['status']

            if not matricula:
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
                    flash('Foto e assinatura atualizadas com sucesso.', 'sucesso')
                    return redirect(url_for('selecionar_e_cadastrar'))
                else:
                    flash('Usuário não encontrado para atualizar fotos.', 'erro')
            except Exception as e:
                flash(f'Erro ao atualizar dados: {e}', 'erro')
            finally:
                cursor.close()
                conexao.close()

      
    return render_template('carteira.html', pessoa=pessoa)


if __name__ == '__main__':
    criar_banco()
    criar_funcionario()
    app.run(host='0.0.0.0', port=5003, debug=True)
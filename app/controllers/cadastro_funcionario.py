from flask import request, redirect, url_for, render_template, flash, session, current_app
from app.controllers.img_to_b64 import imagem_para_base64
from mysql.connector.errors import IntegrityError
from app.controllers.banco import connection
from app.controllers.auditoria.usuario_cadastra_func.usuario_cad_func import auditoria_usuario_cadastrou_funcionario

def cadastro_funcinarios():
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula'].strip()
        nascimento = request.form['nascimento']
        contratacao = request.form['contratacao']
        status = request.form['status']
        identificacao_sexual = request.form['identificacao_sexual']
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
                query = ("INSERT INTO funcionario(usuario_cadastrante,nome,matricula,nascimento,contratacao,status,identificacao_sexual,foto,assinatura) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                valores = (session['user'],nome,matricula,nascimento,contratacao,status,identificacao_sexual,foto_b64,assinatura_b64)

                cursor.execute(query, valores)
                conexao.commit()

                auditoria_usuario_cadastrou_funcionario(session['email'],session['user'],nome,matricula)
                current_app.logger.info(f"Usuario {session['user']} E-mail {session['email']} cadastrou o funcionario {nome} matricula {matricula}.")
                flash('Cadastro realizado com sucesso.', 'sucesso')
            else:
                if pessoa[0]['matricula'] == matricula:
                    current_app.logger.warning(f"Tentativa de cadastro com matricula {matricula} que ja existe.")
                    flash('Usuário já cadastrado com essa matricula.', 'erro')
        
        except IntegrityError as err:
            current_app.logger.error(f"Erro de integridade ao tentar cadastrar funcionario {matricula}: {err}")
            flash(f"Erro de integridade: {err}", 'erro')
        
        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('index.index'))

    
    return render_template('index.html')
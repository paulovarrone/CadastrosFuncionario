from flask import render_template, request, flash, redirect, url_for, current_app, session
from app.controllers.img_to_b64 import imagem_para_base64
from app.controllers.banco import connection
from app.controllers.auditoria.usuario_select.usuario_select_func import auditoria_banco_select_funcionario
from app.controllers.auditoria.usuario_alter_dados_func.usuario_alterou_dados_func import auditoria_usuario_alterou_dados_func

def selecionar_para_cadastrar():
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
                    current_app.logger.warning(f"Funcionario com matricula {matricula} nao encontrado para atualizaçao.")
                    flash('Usuário não encontrado no sistema.', 'erro')
                else:
                    auditoria_banco_select_funcionario(session['email'],session['user'],pessoa['nome'],matricula)
                    current_app.logger.info(f"Usuario {session['user']} E-mail {session['email']} acessou os dados do funcionario {pessoa['nome']} com matricula {matricula}.")
            except Exception as e:
                current_app.logger.error(f'Erro ao buscar funcionario {matricula} para atualizaçao: {e}')
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

            alterou_foto = False
            alterou_assinatura = False

            if not matricula:
                current_app.logger.warning('Matrícula não fornecida para atualização.')
                flash('Matrícula é obrigatória para atualizar fotos.', 'erro')
                return redirect(url_for('carteiradigital.carteiradigital'))

            foto_b64 = imagem_para_base64(foto)
            assinatura_b64 = imagem_para_base64(assinatura)

            try:
                conexao = connection()
                cursor = conexao.cursor(dictionary=True)
                cursor.execute("SELECT * FROM funcionario WHERE matricula = %s", (matricula,))
                pessoa = cursor.fetchone()
                if pessoa:
                    query = "UPDATE funcionario SET foto = %s, assinatura = %s, status = %s, updated_by = %s WHERE matricula = %s"
                    cursor.execute(query, (foto_b64, assinatura_b64,status, session['user'], matricula))
                    conexao.commit()
                    
                    alterou_assinatura, alterou_foto, = "Adicionado", "Adicionado"
                    auditoria_usuario_alterou_dados_func(session['email'], session['user'], nome, matricula, status, alterou_foto, alterou_assinatura)


                    current_app.logger.info(f"Usuario {session['user']} E-mail {session['email']} atualizou os dados de {nome} com matricula {matricula} status {status}")
                    flash('Dados atualizadas com sucesso.', 'sucesso')
                    return redirect(url_for('carteiradigital.carteiradigital'))
                else:
                    current_app.logger.warning(f"Funcionario com matricula {matricula} nao encontrado para atualizacao.")
                    flash('Usuário não encontrado para atualizar dados.', 'erro')
            except Exception as e:
                current_app.logger.error(f'Erro ao atualizar dados do funcionario {matricula}: {e}')
                flash(f'Erro ao atualizar dados: {e}', 'erro')
            finally:
                cursor.close()
                conexao.close()

      
    return render_template('carteira.html', pessoa=pessoa)
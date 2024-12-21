from flask import *
from app.models.banco import *

def selecionar_dados_cadastrais():
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
                current_app.logger.info(f"Usuario {session['user']}, E-mail {session['email']}, selecionou dados do funcionario: {pessoa['nome']} com matricula: {matricula}")
        except Exception as e:
            flash(f"Erro {e}", 'erro')

        finally:
            cursor.close()
            conexao.close()

        return redirect(url_for('selecionarDadosCadastrair.selecionarDadosCadastrair'))

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
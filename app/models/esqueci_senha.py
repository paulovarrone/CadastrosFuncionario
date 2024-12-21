from flask import *
from app.models.banco import *
from app.extensions.bcrypt import bcrypt

def mudar_senha():   
    try:
        conexao = connection()
        cursor = conexao.cursor(dictionary=True)
        
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            cpf = request.form['cpf']
            

            cursor.execute("SELECT * FROM usuario WHERE email = %s AND username = %s ", (email, username))
            usuario_existente = cursor.fetchone()

            

            if usuario_existente:
                hashed_cpf = bcrypt.check_password_hash(usuario_existente['cpf'], cpf)
                if not hashed_cpf:
                    current_app.logger.info(f"Usuario {username}, E-mail {email}, teve tentativa inválida de troca de senha.")
                    flash('Credenciais inválidas. Tente novamente.', 'erro')

                elif password != confirm_password:
                    flash('As senhas não coincidem!', 'erro')
                    current_app.logger.info(f"Usuario {username}, E-mail {email}, teve tentativa inválida de troca de senha.")
                    
                else:
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    
                    query = "UPDATE usuario SET password = %s WHERE username = %s AND email = %s"
                    valores = (hashed_password, username, email)
                    cursor.execute(query, valores)

                    current_app.logger.info(f"Usuario {username}, E-mail {email}, teve sua senha alterado com sucesso.")
                    conexao.commit()
                    flash('Senha alterada com sucesso.', 'sucesso')
                    return redirect(url_for('esqueci_senha.esqueci_senha'))
            else:
                current_app.logger.info(f"Usuario {username}, E-mail {email}, teve tentativa inválida de troca de senha.")
                flash('Credenciais inválidas. Tente novamente.', 'erro')
                return render_template('esqueci_senha.html')
            
    except Exception as e: 
        current_app.logger.error(f"Erro ao trocar senha: {str(e)}")
        flash(f'Erro: {str(e)}', 'erro')
        return render_template('esqueci_senha.html')
    
    finally:
        cursor.close()
        conexao.close()
          
    return render_template('esqueci_senha.html')
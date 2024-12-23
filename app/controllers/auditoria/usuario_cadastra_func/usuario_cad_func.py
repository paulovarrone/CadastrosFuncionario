from app.controllers.banco import connection

def auditoria_usuario_cadastrou_funcionario(email,username,nome,matricula):
    try:    
        conexao = connection()
        cursor = conexao.cursor(dictionary=True)

        query = ("INSERT INTO usuario_cadastrou_funcionario(email_cadastrante,username_cadastrante,nome_funcionario, matricula_funcionario) VALUES(%s,%s,%s,%s)")
        valores = (email,username,nome,matricula)

        cursor.execute(query, valores)
        conexao.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conexao.close()
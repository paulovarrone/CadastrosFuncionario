from app.controllers.banco import connection

def auditoria_banco_select_funcionario(email,username, nome, matricula):
    try:    
        conexao = connection()
        cursor = conexao.cursor(dictionary=True)

        query = ("INSERT INTO usuario_select_funcionario(email,username,nome_funcionario_selecionado, matricula_funcionario_selecionado) VALUES(%s,%s,%s,%s)")
        valores = (email,username,nome,matricula)

        cursor.execute(query, valores)
        conexao.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conexao.close()
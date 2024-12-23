from app.controllers.banco import connection

def auditoria_usuario_alterou_dados_func(email,username,nome,matricula,status,foto,assinatura):
    try:    
        conexao = connection()
        cursor = conexao.cursor(dictionary=True)

        query = ("INSERT INTO usuario_alterou_dados_func(email_user_alterou,username_user_alterou,nome_funcionario, matricula_funcionario,status,foto,assinatura) VALUES(%s,%s,%s,%s,%s,%s,%s)")
        valores = (email,username,nome,matricula,status,foto,assinatura)

        cursor.execute(query, valores)
        conexao.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conexao.close()
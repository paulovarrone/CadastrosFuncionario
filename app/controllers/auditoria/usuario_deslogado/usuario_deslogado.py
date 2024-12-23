from app.controllers.banco import connection

def auditoria_banco_deslogado(email,username):
    try:    
        conexao = connection()
        cursor = conexao.cursor(dictionary=True)

        query = ("INSERT INTO usuario_deslogado(email,username) VALUES(%s,%s)")
        valores = (email,username)

        cursor.execute(query, valores)
        conexao.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conexao.close()
from app.controllers.logs_auditoria import setup_logging
from app.controllers.banco import criar_banco, criar_funcionario, criar_usuario, usuario_alterou_dados_func,usuario_cadastrou_funcionario, usuario_deslogado, usuario_logado, usuario_select_funcionario
from app.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    criar_banco()
    criar_funcionario()
    criar_usuario()
    usuario_select_funcionario()
    usuario_logado()
    usuario_alterou_dados_func()
    usuario_cadastrou_funcionario()
    usuario_deslogado()

    setup_logging(app)
    app.run(host='0.0.0.0', port=5003, debug=True)
from app.controllers.logs_auditoria import setup_logging
from app.controllers.banco import criar_banco, criar_funcionario, criar_usuario
from app.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    criar_banco()
    criar_funcionario()
    criar_usuario()
    setup_logging(app)
    app.run(host='0.0.0.0', port=5003, debug=True)
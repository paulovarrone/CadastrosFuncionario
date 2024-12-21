import base64

def imagem_para_base64(imagem):
    if imagem:
        return base64.b64encode(imagem.read()).decode('utf-8')
    return None
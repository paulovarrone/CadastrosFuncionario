import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:@localhost/recursos_humanos')


def fetch_data_situacao():    
    try:
        query = "SELECT nome, matricula, status, contratacao FROM funcionario"
        df_situacao = pd.read_sql(query, engine)
        return df_situacao
    except Exception as e:
        print(f"Erro ao buscar dados de situação: {e}")
        raise e

def fetch_data_identificacao_sexual():
    try:
        query = "SELECT identificacao_sexual FROM funcionario"
        df_identificacao_sexual = pd.read_sql(query, engine)
        return df_identificacao_sexual
    except Exception as e:
        print(f"Erro ao buscar dados de identificação sexual: {e}")
        raise e

def situacao():
    df = fetch_data_situacao()
    situacao_counts_global = df['status'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(situacao_counts_global, labels=situacao_counts_global.index, autopct='%1.1f%%', startangle=90)
    plt.title('Situação dos funcionários')
    situacao_funcionario = os.path.join('app', 'static', 'imgBI', 'situacao.png')
    plt.savefig(situacao_funcionario)
    plt.close()
    return situacao_funcionario

def identificacao_sexual():
    df = fetch_data_identificacao_sexual()
    identificacao_sexual_counts_global = df['identificacao_sexual'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(identificacao_sexual_counts_global, labels=identificacao_sexual_counts_global.index, autopct='%1.1f%%', startangle=90)
    plt.title('Identificação Sexual dos funcionários')
    identificacao_sexual_funcionario = os.path.join('app', 'static', 'imgBI', 'identificacao.png')
    plt.savefig(identificacao_sexual_funcionario)
    plt.close()
    return identificacao_sexual_funcionario
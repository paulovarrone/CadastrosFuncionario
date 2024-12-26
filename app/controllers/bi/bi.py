import pandas as pd
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine
import plotly.express as px

engine = create_engine('mysql+mysqlconnector://root:@localhost/recursos_humanos')


def fetch_data_situacao():    
    try:
        query = "SELECT nome, matricula, status, contratacao FROM funcionario"
        df_situacao = pd.read_sql(query, engine)
        
        # Converter a coluna 'contratacao' para o tipo datetime, lidando com erros
        df_situacao['contratacao'] = pd.to_datetime(df_situacao['contratacao'], format='%Y-%m-%d', errors='coerce')

        # Substituir valores NaT (datas inválidas) por "Data inválida"
        df_situacao['contratacao'] = df_situacao['contratacao'].dt.strftime('%d/%m/%Y').fillna("Data inválida")
        
        return df_situacao
    except Exception as e:
        print(f"Erro ao buscar dados de situação: {e}")
        raise e


def quantidade_funcionarios():
    try:
        query = """
            SELECT status, COUNT(*) AS quantidade FROM funcionario GROUP BY status;
        """
        df_quantidade_funcionarios = pd.read_sql(query, engine)
        return df_quantidade_funcionarios
    except Exception as e:
        print(f"Erro ao buscar quantidade de funcionários: {e}")
        raise e

def quantidade_identificacao_sexual():
    try:
        query = """
            SELECT identificacao_sexual, COUNT(*) AS quantidade FROM funcionario GROUP BY identificacao_sexual;
        """
        df_identificacao_sexual = pd.read_sql(query, engine)
        return df_identificacao_sexual
    except Exception as e:
        print(f"Erro ao buscar quantidade de identificação sexual: {e}")
        raise e

def fetch_data_identificacao_sexual():
    try:
        query = "SELECT identificacao_sexual FROM funcionario"
        df_identificacao_sexual = pd.read_sql(query, engine)
        return df_identificacao_sexual
    except Exception as e:
        print(f"Erro ao buscar dados de identificação sexual: {e}")
        raise e

# def situacao():
#     df = fetch_data_situacao()
#     situacao_counts_global = df['status'].value_counts()
#     plt.figure(figsize=(6, 6))
#     plt.pie(situacao_counts_global, labels=situacao_counts_global.index, autopct='%1.1f%%', startangle=90)
#     plt.title('Situação dos funcionários')
#     situacao_funcionario = os.path.join('app', 'static', 'imgBI', 'situacao.png')
#     plt.savefig(situacao_funcionario)
#     plt.close()
#     return situacao_funcionario

# def identificacao_sexual():
#     df = fetch_data_identificacao_sexual()
#     identificacao_sexual_counts_global = df['identificacao_sexual'].value_counts()
#     plt.figure(figsize=(6, 6))
#     plt.pie(identificacao_sexual_counts_global, labels=identificacao_sexual_counts_global.index, autopct='%1.1f%%', startangle=90)
#     plt.title('Identificação Sexual dos funcionários')
#     identificacao_sexual_funcionario = os.path.join('app', 'static', 'imgBI', 'identificacao.png')
#     plt.savefig(identificacao_sexual_funcionario)
#     plt.close()
#     return identificacao_sexual_funcionario

def quantidade_funcionarios_plotly():
    try:
        query = "SELECT status, COUNT(*) AS quantidade FROM funcionario GROUP BY status;"
        df_quantidade_funcionarios = pd.read_sql(query, engine)

        # Criar o gráfico interativo com Plotly
        fig = px.pie(
            df_quantidade_funcionarios, 
            names='status', 
            values='quantidade', 
            title='Situação dos Funcionários'
        )
        
        return fig.to_html(full_html=False)  # Retorna o HTML do gráfico para ser renderizado
    except Exception as e:
        print(f"Erro ao buscar quantidade de funcionários: {e}")
        raise e
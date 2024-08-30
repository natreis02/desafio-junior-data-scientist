#  Resolução do desafio de Análise em python dos dados 
"""
analise_python.ipynb

Este script realiza análises sobre os chamados abertos no dia 01/04/2023 na Central de Atendimento 1746 do Rio de Janeiro.
Ele utiliza a biblioteca `basedosdados` e interage com o Google BigQuery para acessar os dados.

Passos:
1. Instalação e importação de pacotes.
2. Autenticação do usuário.
3. Respostas às perguntas sobre os chamados do dia 01/04/2023.

Autor: Natália França dos Reis
"""

# Instalação de pacotes necessários
!pip install basedosdados

!pip install --upgrade google-cloud-bigquery

# Importação de bibliotecas
import pandas as pd

import pandas_gbq

from google.oauth2 import service_account

import basedosdados as bd

from google.cloud import bigquery

# Autenticação do usuário no Google Colab
from google.colab import auth

auth.authenticate_user()

# Credenciais da conta de serviço para BigQuery
credentials_json = {
    "type": "service_account",
    
    "project_id": "new-project-433213",
    
    "private_key_id": "afc761a0ce8074e298d41cd1c8772b5eaa410ecf",
    
    "private_key": "-----BEGIN PRIVATE KEY-----\n<chave_privada_aqui>\n-----END PRIVATE KEY-----\n",
    
    "client_email": "bigquery-access@new-project-433213.iam.gserviceaccount.com",
    
    "client_id": "106010814922063980915",
    
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    
    "token_uri": "https://oauth2.googleapis.com/token",
    
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bigquery-access%40new-project-433213.iam.gserviceaccount.com"
}

# Inicialização do cliente BigQuery
credentials = service_account.Credentials.from_service_account_info(credentials_json)

client = bigquery.Client(credentials=credentials, project='new-project-433213')

# 1. Quantidade de chamados abertos em 01/04/2023
query = """
    SELECT COUNT(*) as total_chamados
    
    FROM `datario.adm_central_atendimento_1746.chamado`
    
    WHERE DATE(data_inicio) = '2023-04-01'
"""
df = client.query(query).to_dataframe()
print("Total de chamados abertos em 01/04/2023:", df['total_chamados'].iloc[0])

# 2. Tipo de chamado com mais registros em 01/04/2023
query = """
    SELECT tipo, COUNT(id_chamado) as total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
    GROUP BY tipo
    ORDER BY total_chamados DESC
    LIMIT 1
"""
df = client.query(query).to_dataframe()

if not df.empty:
    print("Tipo de chamado com mais registros em 01/04/2023:", df['tipo'].iloc[0])
    print("Total de chamados desse tipo:", df['total_chamados'].iloc[0])
else:
    print("Nenhum chamado encontrado para o dia 01/04/2023.")

# 3. Top 3 bairros com mais chamados em 01/04/2023
query_top_bairros = """
    SELECT id_bairro, COUNT(id_chamado) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
    GROUP BY id_bairro
    ORDER BY total_chamados DESC
    LIMIT 3
"""
df_top_bairros = client.query(query_top_bairros).to_dataframe()
print("Top 3 bairros com mais chamados em 01/04/2023:")
print(df_top_bairros)

# Obtenção dos nomes dos bairros
query_bairros_detalhes = """
    SELECT id_bairro, nome
    FROM `datario.dados_mestres.bairro`
"""
df_bairros_detalhes = client.query(query_bairros_detalhes).to_dataframe()
df_merged = df_top_bairros.merge(df_bairros_detalhes, on='id_bairro', how='left')
print("Detalhes dos Top 3 bairros:")
print(df_merged)

# 4. Subprefeitura com mais chamados em 01/04/2023
query = """
    SELECT b.subprefeitura, COUNT(c.id_chamado) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.dados_mestres.bairro` b
    ON c.id_bairro = b.id_bairro
    WHERE DATE(c.data_inicio) = '2023-04-01'
    GROUP BY b.subprefeitura
    ORDER BY total_chamados DESC
    LIMIT 1
"""
df_top_subprefeitura = client.query(query).to_dataframe()
print("Subprefeitura com mais chamados em 01/04/2023:", df_top_subprefeitura)


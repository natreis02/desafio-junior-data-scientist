# -*- coding: utf-8 -*-
"""consulta_query.ipynb

Big Query e Consulta dos dados
"""

# Instalação da biblioteca basedosdados proposta na atividade
!pip install basedosdados

# Instalação do pacote para interagir com o BigQuery
!pip install --upgrade google-cloud-bigquery

# Pacotes necessários
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
import basedosdados as bd
from google.cloud import bigquery

# Autenticação do usuário no Google Colab
from google.colab import auth
auth.authenticate_user()

# Dicionário com as credenciais JSON
credentials_json = {
   "type": "service_account",
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),  
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('GOOGLE_CLIENT_EMAIL')}",
    "universe_domain": "googleapis.com"
}

# Carregar as credenciais da conta de serviço a partir do dicionário JSON
credentials = service_account.Credentials.from_service_account_info(credentials_json)

# Criar o cliente BigQuery com as credenciais e o projeto
project_id = 'new-project-433213'
client = bigquery.Client(credentials=credentials, project=project_id)

# Consultar a primeira tabela
query1 = "SELECT * FROM `datario.adm_central_atendimento_1746.chamado` LIMIT 1000"
df1 = client.query(query1).to_dataframe()

# Consultar a segunda tabela
query2 = "SELECT * FROM `datario.dados_mestres.bairro` LIMIT 1000"
df2 = client.query(query2).to_dataframe()

# Consultar a terceira tabela
query3 = "SELECT * FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` LIMIT 1000"
df3 = client.query(query3).to_dataframe()

# Combinar os DataFrames (Exemplo usando concatenação vertical)
df_combined = pd.concat([df1, df2, df3], ignore_index=True)

# Exibir o DataFrame combinado
print(df_combined.head())

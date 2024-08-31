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
  "project_id": "new-project-433213",
  "private_key_id": "afc761a0ce8074e298d41cd1c8772b5eaa410ecf",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCavdq2T1f07V5A\nycY+pYPVhek7syhweP0yg1A2Kj+x267KgorvmQP2joW3e+rbAgx6hLOKs4CSSR79\nPLKijhtFNLk3FfPLxE7oJZJxJ7ntqLR8k3hJbZvswLjlhTlErlI6YIxzV3VLg95I\nLi8Bd/BJZUwuf25LNCn0HJ2lVvrcDN7Y26v7K/DHuTGfI3fYfqv2DQmcPAJ//Y+0\nbL93qGpUhENs/YtO0YyrifbA1wiZcf99rR5XAhMfThnPIvyKw5vUZMRxDXXzyqmN\nhCtxTr+LWVJU7vTAbD722fVEjJzhqz4LalRpGrBiPBKFJCfdouf0C9yLE4lz3WNv\n/w13CJYLAgMBAAECggEAOkU6IiL4xUPJlW4mGBst7O8zaAbMOKZm+mmWf/8i4zAN\nvzavaRBe/K6ozfJ8+yHnXw+vqJB13yBn6ga8YhhPTp1PDd5XYyk2aZcUcUX7bvJz\nnOHPjx8Wc24TcmLbsPBQCKmo2hpaEijDQL0beFsZAhqCOJRGDU3EaqeH+eYqK0ib\nCJMZyJiRQu157f6YB1KiDkmqAXTTNad4RAyqekhKE3C5f6QgXs/gSP5MZa52kWaN\n+H0UOEwYEtsGCB3rXq4Nyj5n9EVpkong6sdRnUGYgC+aKy7VQz9dJ2Tkc3vfhuhY\nJCSJnk+38GLD3GwosPU2jjzkVReceXmOL92gKz93OQKBgQDYeMwGXao6DKqJmL5t\ntkDlBAoX0oSqD6+VHsawXujObxtB0rbcSmnPG0Wykb1m3AS0CeCDU5hNMDlCcRRj\n7+AVqQEgpfcCrpWASBB3eAvUDq7sYJBCX0sVxZam+rEOzp8VWIKHL6bTw9ngfTnD\nBFT59Xt9sV3lAYL+CQUQYpuRTQKBgQC2/2mmwmvWlOWhwTM3hxfOrJjVhQ7LgOew\ni7OUhGdkQdO3RmGyAV0Deu7ust9KVjuvsCO7pLvaNspPofsuzXl0Dgfy+ajWoBJ3\n8fSokUyRyCkftaSoyzME9h1Pd5b0+o7HF6ni9TQwRFuTJI5HYJ0CchXmEK17sITz\nUELcIsaYtwKBgFEM2YdApq3ZdDjUoeg+JwoYexb0UYvDF8DDpyz+PDiezRvWI3VT\nv042LeBwRPQwSOqIEDHbqNitx6Ki6DmK5OH3R17MBTJR39QKJ3Az2GnrnX8PoLPZ\nLinWs1ON5aFfp5y8aRLoupPrbrZo7KmiA5cbXMNxF3DZIgyvn9/Eq+65AoGANQ8V\nWQ6iKdN+SUo1SXJYCsqsfaxYv9SeWOgIp5VETSNw+YDkrrIKgAnS4U7nwywBnk0Z\n7zwyY3Djc/dpVwaoome3ElIlDCXZdQGoiH+ojdRVaCZImdBg+J1LnlD0ag+D+mH4\nFiA2g5AuZRmCT1vJ6n2dr9lCE8z4n3u0BxPmNT0CgYBpXIETXWJwCLjIexy172C8\nU4Zigif2Zu/1f/NV1DFRjHPSUf9lrde4zH3rZgrD11esbnZMiFeR5XT/xBu0x1LY\nB9O2CzudqNpbXNCZr+Yo+SZ2JINUoQP1ju65ZwSOwg4O0kKgimzVeX42EBO+o7v+\njQBPRiwVt614ovi1XNWnXA==\n-----END PRIVATE KEY-----\n",
  "client_email": "bigquery-access@new-project-433213.iam.gserviceaccount.com",
  "client_id": "106010814922063980915",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bigquery-access%40new-project-433213.iam.gserviceaccount.com",
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

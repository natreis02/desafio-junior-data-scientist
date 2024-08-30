# 🚨 Central de Atendimento 1746 - Análise de Chamados 🚨

Este repositório contém a análise dos chamados registrados pela Central de Atendimento 1746 do Rio de Janeiro, referentes ao dia 01/04/2023. O objetivo desta análise é responder a questões específicas relacionadas a esses registros.

## 🛠️ Ferramentas Utilizadas

- **Python**: A linguagem de programação utilizada para conduzir todas as análises.
- **Basedosdados**: Biblioteca que permite a conexão direta com bases de dados públicas.
- **Google BigQuery**: Plataforma utilizada para o gerenciamento e consulta de grandes volumes de dados.
- **Pandas**: Biblioteca para manipulação e análise de dados.

## 🚀 Como Executar o Script

### 1. Instalação das Bibliotecas Necessárias e conexão com o Big Query
Primeiro, assegure-se a instação das bibliotecas e pacotes essenciais para em seguida, se conectar ao Big Query.

```bash
!pip install basedosdados
!pip install --upgrade google-cloud-bigquery
```
### 2. Importação dos pacotes
```bash
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
import basedosdados as bd
import google.cloud.bigquery as bigquery
```
O processo de autenticação foi realizado para o acesso do usuário a sua conta de e-mail para conceder em seguida, o acesso ao Google Big Query.
### 3. Autenticação
```bash
from google.colab import auth
auth.authenticate_user()
```
Nas configurações de acesso entre Python e Big Query, foi necessário dar permissão ao usuário _bigquery-acess_ e configurá-lo no papel de _Administrador do BigQuery_ e _BigQuery Connection User_.
![acesso](https://github.com/user-attachments/assets/aeeb285a-2fe8-4f9d-acf4-7f97d58fb3fc)

### 4. Configurações das credenciais
Dicionário com as credenciais JSON
```bash
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
```
Após isso, carreguei as credenciais da conta de serviço a partir do dicionário JSON, criei o cliente Big Query com as credenciais e utilizei o id do projeto.
Em seguida, foram realizadas as consultas em cada tabela especificada nos exercícios:

```bash
`datario.adm_central_atendimento_1746.chamado`

`datario.dados_mestres.bairro`

`datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
```
E os dataframes foram combinados e exibidos no código pelo comando `print(df_combined.head())`.

### 📊 Análises Realizadas Análises realizadas
Analisamos a quantidade de chamados abertos, tipos de chamados com mais registros, os bairros com mais chamados e subprefeituras com mais chamados. 
Para a contagem do número de chamados que foram abertos na data 01/04/2023, utilizei a seguinte consulta SQL:
```bash
query = """
    SELECT COUNT(*) as total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
```
Para selecionar o 'tipo', subprefeitura ou 'bairro' com mais chamados, utilizei as seguintes consultas abaixo:
Tipo de chamado
```bash
query = """
    SELECT tipo, COUNT(id_chamado) as total_chamados
    ...
"""
```
Subprefeitura
```bash
query = """
    SELECT b.subprefeitura, COUNT(c.id_chamado) AS total_chamados
    ...
"""
```
Bairro
e
```bash
query_top_bairros = """
    SELECT id_bairro, COUNT(id_chamado) AS total_chamados
    ...
"""
```




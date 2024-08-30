# 🚨 Central de Atendimento 1746 - Análise de Chamados 🚨

Bem-vindo ao repositório de análise de chamados da Central de Atendimento 1746 do Rio de Janeiro! Neste script, vamos explorar os chamados abertos no dia **01/04/2023**, respondendo perguntas intrigantes sobre esses registros. Vamos descobrir juntos os dados por trás dos serviços de atendimento ao cidadão.

## 🛠️ Ferramentas Utilizadas

- **Python**: A linguagem mágica por trás das nossas análises.
- **Basedosdados**: Biblioteca poderosa que conecta diretamente com bases de dados públicas.
- **Google BigQuery**: Nosso portal para grandes volumes de dados.
- **Pandas**: Manipulação e análise de dados, do jeito que a gente gosta!

## 🚀 Como Executar o Script

### 1. Instalação das Bibliotecas Necessárias
Primeiro, assegure-se de que as bibliotecas essenciais estão instaladas:

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
### 3. Autenticação
```bash
from google.colab import auth
auth.authenticate_user()
```
### 4. Configurações das credenciais

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




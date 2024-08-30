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

### 📊 Análises Realizadas 
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
Para selecionar os chamados com o subtipo 'Perturbação do Sossego' durante os eventos, realizamos a consulta selecionando os chamdos da tabela `datario.adm_central_atendimento_1746.chamado` que foram abertos durante os eventos do conjunto de dados `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`. Essa consulta também filtra os eventos que são "Reveillon", "Rock in Rio" e "Carnaval" e considera apenas os chamados nas datas "2022-01-01" e "2023-12-31". A consulta faz uma junção (JOIN) entre a tabela de chamados e a tabela de eventos, usando a condição de que a data de início do chamado `(c.data_inicio)` deve estar entre a data inicial `(e.data_inicial)` e a data final `(e.data_final)` do evento.

```bash
query_chamados_eventos = """
    SELECT COUNT(c.id_chamado) AS total_chamados_eventos
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e
    ON DATE(c.data_inicio) BETWEEN DATE(e.data_inicial) AND DATE(e.data_final)
    WHERE c.subtipo = 'Perturbação do sossego'
    AND e.evento IN ('Reveillon', 'Rock in Rio', 'Carnaval')
    AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
"""
"""
```
# 🌐 Análise de APIs Públicas 🌐
Este repositório contém um notebook Python `analise_api.ipynb` que realiza uma análise utilizando duas APIs públicas: a Public Holiday API e a Open-Meteo Historical Weather API. O objetivo é responder a várias perguntas relacionadas a feriados e condições meteorológicas no Brasil durante o ano de 2024.

## 🔧 Ferramentas Utilizadas
-**Python** : Linguagem de programação utilizada para implementar o código.
-**Google Colab-**: Ambiente onde o código foi desenvolvido e executado.
-**APIs Públicas-**:

-Public Holiday API: Usada para obter informações sobre feriados.
-Open-Meteo Historical Weather API: Utilizada para recuperar dados meteorológicos históricos.

##  🚀 Funcionalidades e como executar o Script
### 1. Importação dos pacotes
Os pacotes utilizados foram:
```bash
import requests
import requests
from collections import defaultdict
from datetime import datetime, timedelta
from collections import Counter
```
### 2. Construção da url do API
A URL final será composta pela combinação da base da URL `https://date.nager.at/api/v3/PublicHolidays/` com o ano e o código do país.
```bash
# Definição de ano e país
country = 'BR'
year = 2024

# Construir a URL da API
url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country}'

# Fazer a requisição
response = requests.get(url)
```
### 🔍 Requisição e Análises 
Este bloco de código verifica se a requisição HTTP feita anteriormente foi bem-sucedida. Se a requisição foi bem-sucedida `status_code` é 200 e o código dentro do bloco `if` será executado.

```bash
# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:

    # Obter os dados da resposta
    holidays = response.json()

    # Contar o número de feriados
    num_holidays = len(holidays)

    print(f'Há {num_holidays} feriados no Brasil em {year}.')
else:
    print('Erro ao obter os dados da API.')
```
`response.json()` converte a resposta da API, que está em formato JSON, em um dicionário (ou lista) Python. Esses dados são então armazenados na variável `holydays`  e por fim os feriados foram retornados pela API.
No código acima foram contados, então, quantos feriados há no Brasil em 2024. 

Em seguida, perguntou-se qual o mês de 2024 tem o maior número de feriados. Para isso, desenvolve-se o seguinte código:

```bash
  # Contar o número de feriados por mês
    holidays_by_month = defaultdict(int)
    for holiday in holidays:
        month = int(holiday['date'].split('-')[1])
        holidays_by_month[month] += 1
```
Onde é criado um dicionário `holidays_by_month`,  usando `defaultdict` do módulo `collections`. O `defaultdict(int)` inicializa qualquer chave nova com o valor 0. Isso é útil para contar o número de feriados por mês sem precisar verificar se a chave já existe no dicionário. Assim,  esse código conta quantos feriados existem em cada mês e armazena essas contagens em um dicionário, onde as chaves são os números dos meses (1 para janeiro, 2 para fevereiro, etc.) e os valores são as quantidades de feriados em cada mês.

Para responder a próxima pergunta, foi adicionado um bloco para contar o número de feriados que caem em dias de semana (segunda a sexta-feira). A data do feriado foi convertida de string para objeto `datatime`
```bash
for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
        if holiday_date.weekday() < 5:  
            weekday_holidays += 1
```
Assim, verifica-se se o feriado cai em um dia de semana e `if holiday_date.weekday() < 5` (onde `weekday()` retorna 0 para segunda-feira e 4 para sexta-feira). O `weekday_holidays += 1` conta os feriados em dia da semana.

Em relação a temperatura média em cada mês, utilizou-se um dicionário `temperatures_by_month` para armazenar as temperaturas diárias em listas, agrupadas por mês. Assim, itera-se sobre cada dia dentro do intervalo de datas `(start_date a end_date)` e adiciona a temperatura diária à lista correspondente ao mês.
Depois, para cada mês, calcula-se a média das temperaturas diárias armazenadas na lista.
```bash
 # Calcular a temperatura média mensal
    temperatures_by_month = {}
    current_date = start_date
    while current_date < end_date:
        month = current_date.month
        if month not in temperatures_by_month:
            temperatures_by_month[month] = []

        temperature = data['daily']['temperature_2m_mean'][current_date.day - 1]
        temperatures_by_month[month].append(temperature)

        current_date += timedelta(days=1)
```
Para a questão 5 foi adicionado um dicionário de códigos de tempo para mapear códigos numéricos para descrições de condições meteorológicas, como "Céu limpo", "Chuva leve", etc. O código conta as ocorrências de cada código de tempo para cada mês usando um `Counter` do módulo `collections`.

```bash
# Determinar o tempo predominante em cada mês
for month, weather_codes in weather_codes_by_month.items():
    if weather_codes:
        most_common_code = Counter(weather_codes).most_common(1)[0][0]
        # Substitua a descrição com o dicionário definido anteriormente
        weather_description = weather_codes_dict.get(most_common_code, f"Código de tempo {most_common_code} não encontrado")
        print(f'Tempo predominante em {month}/{2024}: {weather_description}')
    else:
        print(f'Tempo predominante em {month}/{2024}: Sem dados suficientes')

```
Depois, foi pedido para se considerar algumas suposições, como:
- **O cidadão carioca considera "frio" um dia cuja temperatura média é menor que 20ºC**

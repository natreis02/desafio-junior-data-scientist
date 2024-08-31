# -*- coding: utf-8 -*-
"""analise_python.ipynb

## Instalação de Pacotes, pacotes utilizados e Autenticação do usuário
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

"""## Localização de chamados do 1746

Utilize a tabela de Chamados do 1746 e a tabela de Bairros do Rio de Janeiro para as perguntas de 1-5.

1. Quantos chamados foram abertos no dia 01/04/2023?
"""

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

# Consulta das colunas listadas da tabela relacionada ao central de atendimento
query = """
    SELECT *
    FROM `datario.adm_central_atendimento_1746.chamado`
    LIMIT 10
"""
df = client.query(query).to_dataframe()
print(df.columns)

# Consultar a tabela de Chamados do 1746 para contar os chamados abertos em 01/04/2023
query = """
    SELECT COUNT(*) as total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
"""
df = client.query(query).to_dataframe()

# Total de chamados abertos em 01/04/2023
print("Total de chamados abertos em 01/04/2023:", df['total_chamados'].iloc[0])

"""2. Qual o tipo de chamado que teve mais chamados abertos no dia 01/04/2023?"""

# Consulta para contar os id_chamado por tipo em 01/04/2023
query = """
    SELECT tipo, COUNT(id_chamado) as total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
    GROUP BY tipo
    ORDER BY total_chamados DESC
    LIMIT 1
"""
df = client.query(query).to_dataframe()

# Exibir o tipo de chamado com mais chamados abertos em 01/04/2023 e o total de chamados desse tipo
if not df.empty:
    print("Tipo de chamado com mais chamados abertos em 01/04/2023:", df['tipo'].iloc[0])
    print("Total de chamados desse tipo:", df['total_chamados'].iloc[0])
else:
    print("Nenhum chamado encontrado para o dia 01/04/2023.")

"""3. Quais os nomes dos 3 bairros que mais tiveram chamados abertos nesse dia?"""

# Consulta para contar os 3 bairros com o maior número de chamados em 01/04/2023
query_top_bairros = """
    SELECT id_bairro, COUNT(id_chamado) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE DATE(data_inicio) = '2023-04-01'
    GROUP BY id_bairro
    ORDER BY total_chamados DESC
    LIMIT 3
"""
df_top_bairros = client.query(query_top_bairros).to_dataframe()

# Exibir os resultados
print("Top 3 bairros com o maior número de chamados em 01/04/2023:")
print(df_top_bairros)

# Consultar a tabela de bairros para obter os nomes correspondentes
query_bairros_detalhes = """
    SELECT id_bairro, nome
    FROM `datario.dados_mestres.bairro`
"""
df_bairros_detalhes = client.query(query_bairros_detalhes).to_dataframe()

# Exibir os resultados
print("Detalhes dos bairros:")
print(df_bairros_detalhes)

# Merge dos DataFrames para obter os nomes dos bairros
df_merged = df_top_bairros.merge(df_bairros_detalhes, on='id_bairro', how='left')

# Exibir o DataFrame com os nomes dos bairros
print("Top 3 bairros com o maior número de chamados e seus nomes:")
print(df_merged)

"""4. Qual o nome da subprefeitura com mais chamados abertos nesse dia?"""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Definir a consulta para contar os chamados por subprefeitura em 01/04/2023
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

# Executar a consulta e converter o resultado em um DataFrame
try:
    df_top_subprefeitura = client.query(query).to_dataframe()
    # Exibir os resultados
    print("Subprefeitura com o maior número de chamados em 01/04/2023:")
    print(df_top_subprefeitura)
except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""5. Existe algum chamado aberto nesse dia que não foi associado a um bairro ou subprefeitura na tabela de bairros? Se sim, por que isso acontece?"""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Consultar e contar chamados sem associação a bairros e a subprefeituras
query_chamados_sem_associacao = """
    SELECT COUNT(c.id_chamado) AS total_chamados_sem_associacao
    FROM `datario.adm_central_atendimento_1746.chamado` c
    LEFT JOIN `datario.dados_mestres.bairro` b
    ON c.id_bairro = b.id_bairro
    LEFT JOIN `datario.dados_mestres.subprefeitura` s
    ON b.subprefeitura = s.subprefeitura
    WHERE b.id_bairro IS NULL
    AND s.subprefeitura IS NULL
    AND DATE(c.data_inicio) = '2023-04-01'
"""

try:
    # Executar a consulta e converter o resultado em um DataFrame
    df_chamados_sem_associacao = client.query(query_chamados_sem_associacao).to_dataframe()
    # Exibir os resultados
    print("Número de chamados em 01/04/2023 sem associação a um bairro e uma subprefeitura:")
    print(df_chamados_sem_associacao)
except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""Isso pode ocorrer porque o chamado pode não ter um id_bairro ou subprefeitura registrados, registrados incorretamente com um formato não correspondente ao utilizado nas planilhas.

## Chamados do 1746 em grandes eventos

6. Quantos chamados com o subtipo "Perturbação do sossego" foram abertos desde 01/01/2022 até 31/12/2023 (incluindo extremidades)?
"""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Consultar e contar chamados com o subtipo "Perturbação do sossego" no intervalo de datas
query_chamados_perturbacao = """
    SELECT COUNT(id_chamado) AS total_chamados_perturbacao
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE subtipo = 'Perturbação do sossego'
    AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
"""

try:
    # Executar a consulta e converter o resultado em um DataFrame
    df_chamados_perturbacao = client.query(query_chamados_perturbacao).to_dataframe()
    # Exibir os resultados
    print("Número de chamados com o subtipo 'Perturbação do sossego' de 01/01/2022 a 31/12/2023:")
    print(df_chamados_perturbacao)
except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""7. Selecione os chamados com esse subtipo que foram abertos durante os eventos contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio)."""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Definir a consulta para contar chamados com o subtipo "Perturbação do sossego" durante os eventos
query_chamados_eventos = """
    SELECT COUNT(c.id_chamado) AS total_chamados_eventos
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e
    ON DATE(c.data_inicio) BETWEEN DATE(e.data_inicial) AND DATE(e.data_final)
    WHERE c.subtipo = 'Perturbação do sossego'
    AND e.evento IN ('Reveillon', 'Rock in Rio', 'Carnaval')
    AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
"""

try:
    # Executar a consulta e converter o resultado em um DataFrame
    df_chamados_eventos = client.query(query_chamados_eventos).to_dataframe()

    # Exibir o resultado
    print("Número de chamados com o subtipo 'Perturbação do sossego' durante os eventos entre 01/01/2022 e 31/12/2023:")
    print(df_chamados_eventos)

except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""8. Quantos chamados desse subtipo foram abertos em cada evento?"""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Definir a consulta para contar chamados com o subtipo "Perturbação do sossego" em cada evento
query_chamados_eventos = """
    SELECT e.evento, COUNT(c.id_chamado) AS total_chamados
    FROM `datario.adm_central_atendimento_1746.chamado` c
    JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e
    ON DATE(c.data_inicio) BETWEEN DATE(e.data_inicial) AND DATE(e.data_final)
    WHERE c.subtipo = 'Perturbação do sossego'
    AND e.evento IN ('Reveillon', 'Rock in Rio', 'Carnaval')
    AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
    GROUP BY e.evento
    ORDER BY total_chamados DESC
"""

try:
    # Executar a consulta e converter o resultado em um DataFrame
    df_chamados_eventos = client.query(query_chamados_eventos).to_dataframe()

    # Exibir o resultado
    print("Número de chamados com o subtipo 'Perturbação do sossego' em cada evento entre 01/01/2022 e 31/12/2023:")
    print(df_chamados_eventos)

except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""9. Qual evento teve a maior média diária de chamados abertos desse subtipo?"""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Definir a consulta para calcular a média diária de chamados com o subtipo "Perturbação do sossego" por evento
query_media_diaria = """
    WITH Chamados_Eventos AS (
        SELECT e.evento,
               DATE(e.data_inicial) AS data_inicial,
               DATE(e.data_final) AS data_final,
               COUNT(c.id_chamado) AS total_chamados,
               DATE_DIFF(DATE(e.data_final), DATE(e.data_inicial), DAY) + 1 AS num_dias
        FROM `datario.adm_central_atendimento_1746.chamado` c
        JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e
        ON DATE(c.data_inicio) BETWEEN DATE(e.data_inicial) AND DATE(e.data_final)
        WHERE c.subtipo = 'Perturbação do sossego'
        AND e.evento IN ('Reveillon', 'Rock in Rio', 'Carnaval')
        AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
        GROUP BY e.evento, e.data_inicial, e.data_final
    )
    SELECT evento,
           total_chamados / num_dias AS media_diaria_chamados
    FROM Chamados_Eventos
    ORDER BY media_diaria_chamados DESC
    LIMIT 1
"""

try:
    # Executar a consulta e converter o resultado em um DataFrame
    df_media_diaria = client.query(query_media_diaria).to_dataframe()

    # Exibir o resultado
    print("Evento com a maior média diária de chamados com o subtipo 'Perturbação do sossego':")
    print(df_media_diaria)

except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

"""10. Compare as médias diárias de chamados abertos desse subtipo durante os eventos específicos (Reveillon, Carnaval e Rock in Rio) e a média diária de chamados abertos desse subtipo considerando todo o período de 01/01/2022 até 31/12/2023."""

# Inicializar o cliente BigQuery
client = bigquery.Client(project='new-project-433213')

# Definir a consulta para calcular a média diária de chamados com o subtipo "Perturbação do sossego" durante os eventos específicos
query_media_eventos = """
    WITH Chamados_Eventos AS (
        SELECT e.evento,
               DATE(e.data_inicial) AS data_inicial,
               DATE(e.data_final) AS data_final,
               COUNT(c.id_chamado) AS total_chamados,
               DATE_DIFF(DATE(e.data_final), DATE(e.data_inicial), DAY) + 1 AS num_dias
        FROM `datario.adm_central_atendimento_1746.chamado` c
        JOIN `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos` e
        ON DATE(c.data_inicio) BETWEEN DATE(e.data_inicial) AND DATE(e.data_final)
        WHERE c.subtipo = 'Perturbação do sossego'
        AND e.evento IN ('Reveillon', 'Rock in Rio', 'Carnaval')
        AND DATE(c.data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
        GROUP BY e.evento, e.data_inicial, e.data_final
    )
    SELECT evento,
           total_chamados / num_dias AS media_diaria_chamados
    FROM Chamados_Eventos
"""

# Definir a consulta para calcular a média diária de chamados com o subtipo "Perturbação do sossego" no período total
query_media_total = """
    SELECT
           COUNT(id_chamado) AS total_chamados,
           DATE_DIFF(DATE('2023-12-31'), DATE('2022-01-01'), DAY) + 1 AS num_dias
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE subtipo = 'Perturbação do sossego'
    AND DATE(data_inicio) BETWEEN '2022-01-01' AND '2023-12-31'
"""

try:
    # Executar a consulta para eventos e converter o resultado em um DataFrame
    df_media_eventos = client.query(query_media_eventos).to_dataframe()

    # Executar a consulta para o período total e converter o resultado em um DataFrame
    df_media_total = client.query(query_media_total).to_dataframe()

    # Calcular a média diária para o período total
    df_media_total['media_diaria_chamados'] = df_media_total['total_chamados'] / df_media_total['num_dias']

    # Exibir os resultados
    print("Média diária de chamados com o subtipo 'Perturbação do sossego' durante os eventos específicos:")
    print(df_media_eventos)

    print("\nMédia diária de chamados com o subtipo 'Perturbação do sossego' durante todo o período (01/01/2022 até 31/12/2023):")
    print(df_media_total[['media_diaria_chamados']])

except Exception as e:
    print(f"Erro ao consultar a tabela: {e}")

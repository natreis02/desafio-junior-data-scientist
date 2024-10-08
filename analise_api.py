# -*- coding: utf-8 -*-
"""analise_api.ipynb

Utilize as APIs públicas abaixo para responder às questões 1-8:

*  Public Holiday API
*  Open-Meteo Historical Weather API

1. Quantos feriados há no Brasil em todo o ano de 2024?
"""

# Importar pacotes necessários
import requests
import requests
from collections import defaultdict
from datetime import datetime, timedelta
from collections import Counter

# Definição de ano e país
country = 'BR'
year = 2024

# Construir a URL da API
url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country}'

# Fazer a requisição
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:

    # Obter os dados da resposta
    holidays = response.json()

    # Contar o número de feriados
    num_holidays = len(holidays)

    print(f'Há {num_holidays} feriados no Brasil em {year}.')
else:
    print('Erro ao obter os dados da API.')

"""2. Qual mês de 2024 tem o maior número de feriados?"""

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:

    # Obter os dados da resposta
    holidays = response.json()

    # Contar o número de feriados por mês
    holidays_by_month = defaultdict(int)
    for holiday in holidays:
        month = int(holiday['date'].split('-')[1])
        holidays_by_month[month] += 1

    # Encontrar o mês com o maior número de feriados
    max_month = max(holidays_by_month, key=holidays_by_month.get)
    max_holidays = holidays_by_month[max_month]

    print(f'O mês {max_month} tem o maior número de feriados em {year}, com {max_holidays} feriados.')
else:
    print('Erro ao obter os dados da API.')

"""3. Quantos feriados em 2024 caem em dias de semana (segunda a sexta-feira)?"""

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obter os dados da resposta
    holidays = response.json()

    # Contar o número de feriados em dias de semana
    weekday_holidays = 0
    for holiday in holidays:
        holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')
        if holiday_date.weekday() < 5:  # 0 = segunda-feira, 4 = sexta-feira
            weekday_holidays += 1

    print(f'Há {weekday_holidays} feriados em 2024 que caem em dias de semana (segunda a sexta-feira) no Brasil.')
else:
    print('Erro ao obter os dados da API.')

"""4. Qual foi a temperatura média em cada mês?
*Utilize a Open-Meteo Historical Weather API para obter as temperaturas médias diárias no Rio de Janeiro de 01/01/2024 a 01/08/2024.*
"""

# Definir a localização e o período
latitude = -22.9068
longitude = -43.1729
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 8, 1)

# Construir a URL da API
url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date.strftime("%Y-%m-%d")}&end_date={end_date.strftime("%Y-%m-%d")}&daily=temperature_2m_mean&timezone=America%2FSao_Paulo'

# Fazer a requisição
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obter os dados da resposta
    data = response.json()

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

    # Calcular a temperatura média de cada mês
    for month, temps in temperatures_by_month.items():
        avg_temp = sum(temps) / len(temps)
        print(f'Temperatura média em {month}/{2024}: {avg_temp:.2f}°C')
else:
    print('Erro ao obter os dados da API.')

"""5. Qual foi o tempo predominante em cada mês nesse período?

*Utilize como referência para o código de tempo (weather_code) o seguinte link: WMO Code.*
"""

# Definir a localização e o período
latitude = -22.9068
longitude = -43.1729
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 8, 1)

# Construir a URL da API
url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date.strftime("%Y-%m-%d")}&end_date={end_date.strftime("%Y-%m-%d")}&daily=weathercode&timezone=America%2FSao_Paulo'

# Fazer a requisição
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obter os dados da resposta
    data = response.json()

    # Calcular o tempo predominante mensal
    weather_by_month = {}
    current_date = start_date
    while current_date < end_date:
        month = current_date.month
        if month not in weather_by_month:
            weather_by_month[month] = []

        weather_code = data['daily']['weathercode'][current_date.day - 1]
        weather_by_month[month].append(weather_code)

        current_date += timedelta(days=1)

    # Definir um dicionário para mapear os códigos de tempo para descrições
    weather_descriptions = {
       0: "Céu limpo",
    1: "Céu parcialmente nublado",
    2: "Nublado",
    3: "Nevoeiro",
    45: "Neblina",
    48: "Geada de deposição",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa densa",
    56: "Garoa congelante leve",
    57: "Garoa congelante densa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva congelante leve",
    67: "Chuva congelante forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Neve granulada",
    80: "Chuva de verão leve",
    81: "Chuva de verão moderada",
    82: "Chuva de verão forte",
    85: "Neve de verão leve",
    86: "Neve de verão forte",
    95: "Tempestade com trovões",
    96: "Tempestade com granizo leve",
    99: "Tempestade com granizo forte"
    }

    # Calcular o tempo predominante de cada mês
    for month, codes in weather_by_month.items():
        predominant_weather = max(set(codes), key=codes.count)
        description = weather_descriptions.get(predominant_weather, "Desconhecido")
        print(f'Tempo predominante em {month}/2024: {description}')
else:
    print('Erro ao obter os dados da API.')

"""6. Qual foi o tempo e a temperatura média em cada feriado de 01/01/2024 a 01/08/2024?"""

# Dicionário de feriados com as datas e nomes
feriados = {
    "Confraternização Universal": datetime(2024, 1, 1),
    "Carnaval (Segunda-feira)": datetime(2024, 2, 12),
    "Carnaval (Terça-feira)": datetime(2024, 2, 13),
    "Sexta-feira Santa": datetime(2024, 3, 29),
    "Tiradentes": datetime(2024, 4, 21),
    "Dia do Trabalho": datetime(2024, 5, 1)
}

# Dicionário de códigos de tempo
weather_codes_dict = {
    0: "Céu limpo",
    1: "Céu parcialmente nublado",
    2: "Nublado",
    3: "Nevoeiro",
    45: "Neblina",
    48: "Geada de deposição",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa densa",
    56: "Garoa congelante leve",
    57: "Garoa congelante densa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva congelante leve",
    67: "Chuva congelante forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Neve granulada",
    80: "Chuva de verão leve",
    81: "Chuva de verão moderada",
    82: "Chuva de verão forte",
    85: "Neve de verão leve",
    86: "Neve de verão forte",
    95: "Tempestade com trovões",
    96: "Tempestade com granizo leve",
    99: "Tempestade com granizo forte"
}

# Loop pelos feriados para obter as informações climáticas
for nome_feriado, data_feriado in feriados.items():
    # Construir a URL da API para cada feriado
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={data_feriado.strftime("%Y-%m-%d")}&end_date={data_feriado.strftime("%Y-%m-%d")}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America%2FSao_Paulo'

    # Fazer a requisição
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obter os dados da resposta
        data = response.json()

        # Extrair as temperaturas e o código de tempo
        max_temp = data['daily']['temperature_2m_max'][0]
        min_temp = data['daily']['temperature_2m_min'][0]
        weather_code = data['daily']['weathercode'][0]

        # Calcular a temperatura média
        avg_temp = (max_temp + min_temp) / 2

        # Exibir as informações
        weather_desc = weather_codes_dict.get(weather_code, "Código de tempo desconhecido")
        print(f'{nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}):')
        print(f'Tempo: {weather_desc}')
        print(f'Temperatura média: {avg_temp:.1f}°C\n')
    else:
        print(f'Erro ao obter os dados para {nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}).')

"""7. Considere as seguintes suposições:

*   O cidadão carioca considera "frio" um dia cuja temperatura média é menor que 20ºC;
*   Um feriado bem aproveitado no Rio de Janeiro é aquele em que se pode ir à praia;
*   O cidadão carioca só vai à praia quando não está com frio;
*   O cidadão carioca também só vai à praia em dias com sol, evitando dias totalmente nublados ou chuvosos (considere weather_code para determinar as condições climáticas).

Houve algum feriado "não aproveitável" em 2024? Se sim, qual(is)?
"""

# Loop pelos feriados para obter as informações climáticas
for nome_feriado, data_feriado in feriados.items():

    # Construir a URL da API para cada feriado
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={data_feriado.strftime("%Y-%m-%d")}&end_date={data_feriado.strftime("%Y-%m-%d")}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America%2FSao_Paulo'

    # Fazer a requisição
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obter os dados da resposta
        data = response.json()

        # Extrair as temperaturas e o código de tempo
        max_temp = data['daily']['temperature_2m_max'][0]
        min_temp = data['daily']['temperature_2m_min'][0]
        weather_code = data['daily']['weathercode'][0]

        # Calcular a temperatura média
        avg_temp = (max_temp + min_temp) / 2

        # Verificar se o feriado foi "não aproveitável"
        weather_desc = weather_codes_dict.get(weather_code, "Código de tempo desconhecido")
        enjoyable_climate = {0,1}
        if avg_temp < 20 or weather_code not in enjoyable_climate:
            print(f'{nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}):')
            print(f'Tempo: {weather_desc}')
            print(f'Temperatura média: {avg_temp:.1f}°C')
            print('Resultado: Feriado "não aproveitável"\n')
        else:
            print(f'{nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}):')
            print(f'Tempo: {weather_desc}')
            print(f'Temperatura média: {avg_temp:.1f}°C')
            print('Resultado: Feriado aproveitável\n')
    else:
        print(f'Erro ao obter os dados para {nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}).')

"""Os feriados não aproveitáveis foram: Confraternização Universal, Carnaval (Terça-feira), Sexta-feira Santa e Tiradentes.

8. Qual foi o feriado "mais aproveitável" de 2024?

*Considere o melhor par tempo e temperatura.*
"""

# Variáveis para armazenar o feriado mais aproveitável
feriado_mais_aproveitavel = None
melhor_tempo = None
melhor_temperatura_media = None

# Loop pelos feriados para obter as informações climáticas
for nome_feriado, data_feriado in feriados.items():
    # Construir a URL da API para cada feriado
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={data_feriado.strftime("%Y-%m-%d")}&end_date={data_feriado.strftime("%Y-%m-%d")}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=America%2FSao_Paulo'

    # Fazer a requisição
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obter os dados da resposta
        data = response.json()

        # Extrair as temperaturas e o código de tempo
        max_temp = data['daily']['temperature_2m_max'][0]
        min_temp = data['daily']['temperature_2m_min'][0]
        weather_code = data['daily']['weathercode'][0]

        # Calcular a temperatura média
        avg_temp = (max_temp + min_temp) / 2

        # Verificar se este feriado é o mais aproveitável
        if (melhor_tempo is None or weather_code < melhor_tempo) and avg_temp > 20:
            feriado_mais_aproveitavel = nome_feriado
            melhor_tempo = weather_code
            melhor_temperatura_media = avg_temp

    else:
        print(f'Erro ao obter os dados para {nome_feriado} ({data_feriado.strftime("%d/%m/%Y")}).')

# Exibir o feriado mais aproveitável
if feriado_mais_aproveitavel:
    print(f'O feriado mais aproveitável de 2024 foi: {feriado_mais_aproveitavel}')
    print(f'Temperatura média: {melhor_temperatura_media:.1f}°C')
    print(f'Condições climáticas: {weather_codes_dict[melhor_tempo]}')
else:
    print('Não foi possível determinar o feriado mais aproveitável.')

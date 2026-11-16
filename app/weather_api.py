
import requests


def obter_clima_atual():
    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "current": "temperature_2m,relative_humidity_2m",
        "timezone": "America/Sao_Paulo"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=10
        )

        resposta.raise_for_status()

        dados = resposta.json()
        atual = dados["current"]

        return {
            "location": "São Paulo - SP",
            "temperature": atual["temperature_2m"],
            "humidity": atual["relative_humidity_2m"],
            "measured_at": atual["time"]
        }

    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao consultar Open-Meteo: {erro}")
        return None


def obter_qualidade_ar():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    parametros = {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "current": "european_aqi",
        "timezone": "America/Sao_Paulo"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=10
        )

        resposta.raise_for_status()

        dados = resposta.json()
        atual = dados["current"]

        return {
            "location": "São Paulo - SP",
            "air_quality": atual["european_aqi"],
            "measured_at": atual["time"],
            "index_type": "EAQI"
        }

    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao consultar qualidade do ar: {erro}")
        return None

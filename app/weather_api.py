
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Carrega a chave da WeatherAPI
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

# Cache de 15 minutos
CACHE_TEMPO = 15 * 60

cache_clima = {
    "dados": None,
    "atualizado_em": 0,
    "bloqueado_ate": 0
}


def consultar_weatherapi():
    """API alternativa para temperatura e umidade."""

    if not WEATHERAPI_KEY:
        print("WeatherAPI: chave não configurada.")
        return None

    url = "https://api.weatherapi.com/v1/current.json"

    parametros = {
        "key": WEATHERAPI_KEY,
        "q": "-23.5505,-46.6333",
        "aqi": "no"
    }

    try:
        resposta = requests.get(
            url,
            params=parametros,
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()
        atual = dados["current"]

        return {
            "location": "São Paulo - SP",
            "temperature": atual["temp_c"],
            "humidity": atual["humidity"],
            "measured_at": atual["last_updated"]
        }

    except (requests.RequestException, KeyError, ValueError) as erro:
        print(
            "Erro ao consultar WeatherAPI:",
            type(erro).__name__
        )
        return None


def obter_clima_atual():
    """Consulta Open-Meteo e utiliza WeatherAPI como alternativa."""

    agora = time.time()

    # Reutiliza dados enquanto o cache estiver válido
    if (
        cache_clima["dados"] is not None
        and agora - cache_clima["atualizado_em"] < CACHE_TEMPO
    ):
        return cache_clima["dados"].copy()

    # Evita consultar Open-Meteo durante bloqueio
    if agora >= cache_clima["bloqueado_ate"]:

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
                timeout=15
            )

            if resposta.status_code == 429:
                print("Open-Meteo: limite de requisições atingido.")
                cache_clima["bloqueado_ate"] = (
                    time.time() + CACHE_TEMPO
                )
            else:
                resposta.raise_for_status()

                dados = resposta.json()
                atual = dados["current"]

                resultado = {
                    "location": "São Paulo - SP",
                    "temperature": atual["temperature_2m"],
                    "humidity": atual["relative_humidity_2m"],
                    "measured_at": atual["time"]
                }

                cache_clima["dados"] = resultado.copy()
                cache_clima["atualizado_em"] = time.time()
                cache_clima["bloqueado_ate"] = 0

                print("Clima obtido pela Open-Meteo.")
                return resultado

        except (requests.RequestException, KeyError, ValueError) as erro:
            print(
                "Erro ao consultar Open-Meteo:",
                type(erro).__name__
            )

    # Tenta a API alternativa
    resultado = consultar_weatherapi()

    if resultado is not None:
        cache_clima["dados"] = resultado.copy()
        cache_clima["atualizado_em"] = time.time()

        print("Clima obtido pela WeatherAPI.")
        return resultado

    # Último recurso: dados anteriores
    if cache_clima["dados"] is not None:
        print("Utilizando últimos dados meteorológicos disponíveis.")
        return cache_clima["dados"].copy()

    return None


def obter_qualidade_ar():
    """Consulta o índice europeu de qualidade do ar."""

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
        print(
            "Erro ao consultar qualidade do ar:",
            type(erro).__name__
        )
        return None

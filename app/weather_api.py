
import time
import requests

CACHE_TEMPO = 15 * 60  # 15 minutos
cache_clima = {
    "dados": None,
    "atualizado_em": 0,
    "bloqueado_ate": 0
}


def obter_clima_atual():
    agora = time.time()

    # Reutiliza os dados enquanto o cache estiver válido.
    if (
        cache_clima["dados"] is not None
        and agora - cache_clima["atualizado_em"] < CACHE_TEMPO
    ):
        return cache_clima["dados"].copy()

    # Evita novas chamadas durante bloqueios temporários.
    if agora < cache_clima["bloqueado_ate"]:
        return (
            cache_clima["dados"].copy()
            if cache_clima["dados"] is not None
            else None
        )

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
            cache_clima["bloqueado_ate"] = agora + CACHE_TEMPO

            return (
                cache_clima["dados"].copy()
                if cache_clima["dados"] is not None
                else None
            )

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

        return resultado

    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao consultar Open-Meteo: {erro}")

        return (
            cache_clima["dados"].copy()
            if cache_clima["dados"] is not None
            else None
        )


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


import logging
import threading
from datetime import datetime

from app.database import get_connection
from app.weather_api import obter_clima_atual, obter_qualidade_ar

logger = logging.getLogger(__name__)


def coletar_e_salvar():
    """Consulta as APIs e registra uma medição por hora."""

    agora = datetime.now().astimezone()
    hora_registro = agora.strftime("%Y-%m-%dT%H:00")

    dados = obter_clima_atual()

    if dados is None:
        logger.warning("EcoPulse: não foi possível obter o clima.")
        return

    qualidade = obter_qualidade_ar()
    indice_ar = qualidade["air_quality"] if qualidade else None

    connection = get_connection()

    try:
        connection.execute("""
            INSERT OR IGNORE INTO weather_measurements
            (temperature, humidity, air_quality, location, measured_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            dados["temperature"],
            dados["humidity"],
            indice_ar,
            dados["location"],
            hora_registro
        ))

        connection.commit()
        logger.info("EcoPulse: coleta concluída às %s", hora_registro)

    except Exception:
        connection.rollback()
        logger.exception("EcoPulse: erro ao salvar medição.")

    finally:
        connection.close()


def iniciar_coleta():
    """Inicia a coleta em segundo plano, uma vez por hora."""

    def executar():
        coletar_e_salvar()

        while True:
            agora = datetime.now().astimezone()
            segundos_ate_proxima_hora = (
                3600 - (agora.minute * 60 + agora.second)
                - agora.microsecond / 1_000_000
            )

            if segundos_ate_proxima_hora <= 0:
                segundos_ate_proxima_hora = 3600

            threading.Event().wait(segundos_ate_proxima_hora)
            coletar_e_salvar()

    thread = threading.Thread(target=executar, daemon=True)
    thread.start()

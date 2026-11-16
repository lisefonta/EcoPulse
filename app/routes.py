
from flask import Blueprint, jsonify, request, render_template
from app.database import get_connection
from app.weather_api import obter_clima_atual, obter_qualidade_ar

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/measurements", methods=["POST"])
def create_measurement():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "erro": "Envie os dados em formato JSON"
        }), 400

    required_fields = [
        "temperature",
        "humidity",
        "air_quality",
        "location"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({
            "erro": "Todos os campos são obrigatórios"
        }), 400

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        air_quality = float(data["air_quality"])
        location = str(data["location"]).strip()

        if not location:
            raise ValueError()

        if not 0 <= humidity <= 100:
            return jsonify({
                "erro": "A umidade deve estar entre 0 e 100"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "erro": "Valores informados são inválidos"
        }), 400

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO measurements
            (temperature, humidity, air_quality, location)
            VALUES (?, ?, ?, ?)
        """, (
            temperature,
            humidity,
            air_quality,
            location
        ))

        connection.commit()

    finally:
        connection.close()

    return jsonify({
        "mensagem": "Medição cadastrada com sucesso!"
    }), 201


@main.route("/measurements", methods=["GET"])
def get_measurements():
    connection = get_connection()

    try:
        measurements = connection.execute("""
            SELECT *
            FROM measurements
            ORDER BY id DESC
        """).fetchall()

        return jsonify([
            dict(item) for item in measurements
        ]), 200

    finally:
        connection.close()


@main.route("/weather", methods=["GET"])
def get_weather():
    """
    Consulta os dados meteorológicos atuais.
    Não grava registros no histórico.
    """

    dados = obter_clima_atual()

    if dados is None:
        return jsonify({
            "erro": "Não foi possível consultar os dados meteorológicos"
        }), 503

    qualidade = obter_qualidade_ar()

    dados["air_quality"] = (
        qualidade["air_quality"]
        if qualidade is not None
        else None
    )

    return jsonify(dados), 200


@main.route("/weather/history", methods=["GET"])
def get_weather_history():
    """
    Retorna as medições armazenadas no SQLite.
    """

    connection = get_connection()

    try:
        measurements = connection.execute("""
            SELECT *
            FROM weather_measurements
            ORDER BY measured_at ASC
        """).fetchall()

        return jsonify([
            dict(item) for item in measurements
        ]), 200

    finally:
        connection.close()


@main.route("/air-quality", methods=["GET"])
def get_air_quality():
    dados = obter_qualidade_ar()

    if dados is None:
        return jsonify({
            "erro": "Não foi possível consultar a qualidade do ar"
        }), 503

    return jsonify(dados), 200

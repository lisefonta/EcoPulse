
import sqlite3
from pathlib import Path

# Caminho da pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do banco de dados
DATABASE = BASE_DIR / "data" / "ecopulse.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    try:
        # Tabela original: medições cadastradas
        connection.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                air_quality REAL NOT NULL,
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de medições meteorológicas reais
        connection.execute("""
            CREATE TABLE IF NOT EXISTS weather_measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                air_quality REAL,
                location TEXT NOT NULL,
                measured_at TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(location, measured_at)
            )
        """)

        # Atualiza bancos existentes sem apagar registros
        columns = [
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(weather_measurements)"
            ).fetchall()
        ]

        if "air_quality" not in columns:
            connection.execute("""
                ALTER TABLE weather_measurements
                ADD COLUMN air_quality REAL
            """)

        connection.commit()

    finally:
        connection.close()

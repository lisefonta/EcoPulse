
from app import create_app
from app.collector import iniciar_coleta

app = create_app()

if __name__ == "__main__":
    iniciar_coleta()
    app.run(debug=True, use_reloader=False)

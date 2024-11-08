from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Asegúrate de que debug=True esté configurado
from app import create_app, db
from app.models import User, OAuth

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("¡Tablas creadas exitosamente!")
    except Exception as e:
        print("Error al crear las tablas:", str(e))
        
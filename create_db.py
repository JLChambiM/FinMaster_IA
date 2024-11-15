from app import create_app, db
from app.models import User, Survey, FinancialProfile, OAuth

app = create_app()

with app.app_context():
    try:
        # Eliminar todas las tablas existentes
        db.drop_all()
        print("¡Tablas eliminadas exitosamente!")
        
        # Crear las tablas nuevamente
        db.create_all()
        print("¡Tablas creadas exitosamente!")
        
        # Verificar las tablas creadas
        print("\nTablas en la base de datos:")
        for table in db.metadata.tables.keys():
            print(f"- {table}")
            
    except Exception as e:
        print("Error al crear las tablas:", str(e))
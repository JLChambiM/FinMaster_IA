from app import create_app, db
from app.models import User, Survey, FinancialProfile, OAuth, LearningGoal

app = create_app()

with app.app_context():
    try:
        db.drop_all()  # Esto eliminará todas las tablas, incluyendo financial_goal
        print("¡Tablas eliminadas exitosamente!")
        
        db.create_all()  # Creará las nuevas tablas, incluyendo learning_goal
        print("¡Tablas creadas exitosamente!")
        
        # Verificar las tablas creadas
        print("\nTablas en la base de datos:")
        for table in db.metadata.tables.keys():
            print(f"- {table}")
            
    except Exception as e:
        print("Error al crear las tablas:", str(e))
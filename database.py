from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import base

engine = create_engine('sqlite:///tarea_misiones.db')
SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database():
    # Crea todas las tablas en la base de datos
    base.metadata.create_all(bind=engine)

# Ejecuta para crear la base de datos
create_database()
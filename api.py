from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from modelos import Personaje, Mision, PersonajeMision

app = FastAPI()


@app.post("/personajes")
def crear_personaje(nombre,db: Session = Depends(get_db)):
    nuevo_personaje = Personaje(nombre=nombre, nivel=1, experiencia=0)
    db.add(nuevo_personaje)
    db.commit()
    db.refresh(nuevo_personaje)
    return {"message": "Personaje creado", "personaje": nuevo_personaje.nombre}

@app.post("/misiones")
def crear_mision(nombre, descripcion, experiencia, db: Session = Depends(get_db)):
    nueva_mision = Mision(nombre=nombre, descripcion=descripcion, experiencia=experiencia, estado='pendiente')
    db.add(nueva_mision)
    db.commit()
    db.refresh(nueva_mision)
    return {"message": "Misión creada", "mision": nueva_mision.nombre}
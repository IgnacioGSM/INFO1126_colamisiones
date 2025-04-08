from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from modelos import Personaje, Mision, PersonajeMision
from Cola import encolar_mision, completar_mision, listar_misiones

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

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def encolar_mision_api(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    # Verificar si el personaje y la misión existen
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    mision = db.query(Mision).filter(Mision.id == mision_id).first()
    if not personaje:
        return {"message": "Personaje no encontrado"}
    if not mision:
        return {"message": "Misión no encontrada"}
    
    # Verificar si la misión está pendiente
    if mision.estado != 'pendiente':
        return {"message": "La misión ya ha sido completada"}
    
    # Verificar si el personaje ya tiene la misión
    mision_existente = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id, PersonajeMision.mision_id == mision_id).first()
    if mision_existente:
        return {"message": "La misión ya está encolada para este personaje"}
    
    # Encolar la misión
    resultado = encolar_mision(db, personaje_id, mision_id)
    return resultado

@app.post("/personajes/{personaje_id}/completar")
def completar_mision_api(personaje_id: int, db: Session = Depends(get_db)):
    # Verificar si el personaje existe
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not personaje:
        return {"message": "Personaje no encontrado"}
    
    # Completar la primera misión en la cola del personaje
    resultado = completar_mision(db, personaje_id)
    # si no hay misiones el resultado lo dirá
    return resultado

@app.get("/personajes/{personaje_id}/misiones")
def obtener_misiones_personaje(personaje_id: int, db: Session = Depends(get_db)):
    # Verificar si el personaje existe
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if not personaje:
        return {"message": "Personaje no encontrado"}
    
    # Listar las misiones en la cola del personaje
    misiones = listar_misiones(db, personaje_id)
    return misiones
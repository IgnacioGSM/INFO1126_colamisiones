# Operaciones que afectan a la base de datos usando la logica de una estructura FIFO
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from modelos import Personaje, Mision, PersonajeMision

def tiene_misiones(db, personaje_id):   # is_empty
    # Verifica si el personaje tiene misiones en la cola
    misiones = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id).first()
    return misiones is not None

def cantidad_misiones(db, personaje_id):   # size
    # Devuelve la cantidad de misiones en la cola del personaje
    misiones = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id).all()
    return len(misiones)

def encolar_mision(db, personaje_id, mision_id):
    # Primero verificar cuantas misiones tiene el personaje
    orden = db.query(func.max(PersonajeMision.orden)).filter(PersonajeMision.personaje_id == personaje_id).scalar() # scalar devuelve un solo valor o None
    if orden is None:
        orden = 1   # primera mision
    else:
        orden += 1

    # Crear la relación entre el personaje y la misión
    relacion = PersonajeMision(personaje_id=personaje_id, mision_id=mision_id, orden=orden)
    db.add(relacion)
    db.commit()
    db.refresh(relacion)
    return {"message": "Misión encolada", "personaje_id": personaje_id, "mision_id": mision_id, "orden": orden}

def completar_mision(db, personaje_id):
    # Obtener la primera misión en la cola del personaje
    mision_relacion = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id).first() # Devolverá la primera misión en la cola o None si no hay misiones
    if not mision_relacion:
        return {"message": "No hay misiones en la cola para este personaje"}
    
    # Obtener la misión asociada
    mision = db.query(Mision).filter(Mision.id == mision_relacion.mision_id).first()
    if not mision:
        return {"message": "Misión no encontrada"}
    
    # Completar la misión
    mision.estado = 'completada'
    db.commit()
    # Eliminar la relación de la misión del personaje
    db.delete(mision_relacion)
    db.commit()

    # Actualizar la experiencia del personaje
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if personaje:
        personaje.experiencia += mision.experiencia
        db.commit()
        db.refresh(personaje)
        while personaje.experiencia >= 100:
            personaje.nivel += 1
            personaje.experiencia -= 100
            db.commit()
            db.refresh(personaje)
    else:
        return {"message": "Personaje no encontrado"}

    return {"message": "Misión completada", "mision_id": mision.id, "completada por el personaje con id:": personaje_id}


def listar_misiones(db, personaje_id):
    # Obtiene todas las misiones en el orden de la cola
    misiones = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id).order_by(PersonajeMision.orden).all()
    if not misiones:
        return {"message": "No hay misiones en la cola para este personaje"}
    
    # Obtener los detalles de las misiones
    misiones_detalles = []
    orden_personal = 0
    for mision_relacion in misiones:
        mision = db.query(Mision).filter(Mision.id == mision_relacion.mision_id).first()
        if mision:
            orden_personal += 1
            misiones_detalles.append({
                "mision_id": mision.id,
                "nombre": mision.nombre,
                "descripcion": mision.descripcion,
                "orden": orden_personal
            })
    return {"misiones": misiones_detalles}

def mostrar_primera_mision(db, personaje_id):           # first
    # Obtener la primera misión en la cola del personaje
    mision_relacion = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == personaje_id).first() # Devolverá la primera misión en la cola o None si no hay misiones
    if not mision_relacion:
        return {"message": "No hay misiones en la cola para este personaje"}
    
    # Obtener la misión asociada
    mision = db.query(Mision).filter(Mision.id == mision_relacion.mision_id).first()
    if not mision:
        return {"message": "Misión no encontrada"}
    
    return {
        "mision_id": mision.id,
        "nombre": mision.nombre,
        "descripcion": mision.descripcion,
        "estado": mision.estado
    }
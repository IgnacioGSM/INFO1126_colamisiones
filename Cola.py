# Operaciones que afectan a la base de datos usando la logica de una estructura FIFO
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from modelos import Personaje, Mision, PersonajeMision

# Estas funciones se activaran una vez se haya verificado que el personaje y la misión existen

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
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class Personaje(base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    nivel = Column(Integer, nullable=False)
    experiencia = Column(Integer, nullable=False)

    # Relacion con PersonajeMision
    misiones = relationship("PersonajeMision", back_populates="personaje")

class Mision(base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=False)
    experiencia = Column(Integer, nullable=False)
    estado = Column(Enum('pendiente', 'completada', name='estados'), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())   # func.now() le dirá al motor de base de datos que use la fecha y hora actuales

    # Relacion con PersonajeMision
    personajes = relationship("PersonajeMision", back_populates="mision")


# Tabla intermedia para la relación muchos a muchos
class PersonajeMision(base):
    __tablename__ = 'personajes_misiones'
    personaje_id = Column(Integer, ForeignKey('personajes.id'), primary_key=True)
    mision_id = Column(Integer, ForeignKey('misiones.id'), primary_key=True)

    # Relaciones inversas
    personaje = relationship("Personaje", back_populates="misiones")    # back popula el nombre de la relación en la clase Personaje
    mision = relationship("Mision", back_populates="personajes")
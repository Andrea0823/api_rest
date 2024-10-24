from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://user:VGqWJEUZnvN093CJGfisqyHuWCT8qk6X@dpg-cscu8vhu0jms73cms8c0-a.oregon-postgres.render.com/db_agenda_sd8j_jh6p"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Personas(Base):
    __tablename__ = "usuarios"

    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    telefono = Column(String(100), unique=True, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class PersonaCreate(BaseModel):
    nombre: str
    telefono: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/personas/", response_model=PersonaCreate)
def crear_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = Personas(nombre=persona.nombre, telefono=persona.telefono)
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

@app.get("/personas/", response_model=List[PersonaCreate])
def obtener_personas(db: Session = Depends(get_db)):
    personas = db.query(Personas).all()
    return personas

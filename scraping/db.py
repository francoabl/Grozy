from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/grozy"  # ⚠️ Cambia usuario, clave y host

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    precio = Column(Float)
    enlace = Column(Text)
    supermercado = Column(String(100))
    imagen_url = Column(Text)

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)

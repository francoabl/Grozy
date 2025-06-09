from sqlalchemy import String, Integer, Column 
from database import Base


class Ingreso (Base):
    ____tablename___="producto"
    id_producto = Column (Integer, primary_key=True, index=True) 
    nombre_producto = Column(String (200))
    link_producto = Column (String(500))
from db import SessionLocal, Producto

db = SessionLocal()
nuevo = Producto(
    nombre="Producto de prueba",
    precio=1990,
    enlace="https://prueba.com",
    supermercado="Test",
    imagen_url="https://imagen.com"
)
db.add(nuevo)
db.commit()
db.close()
print("Inserción exitosa")
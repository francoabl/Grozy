import csv
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from db import SessionLocal, Producto  # <-- Importa tu modelo y sesión

# Configurar Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Opcional: no abre ventana
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL del sitio
url = 'https://www.santaisabel.cl/desayuno/cereales-avenas-y-barras?page=1'
driver.get(url)
sleep(5)  # Espera a que cargue todo

# Extraer elementos
productos = []
def scrapeo():
    nombres = driver.find_elements(By.XPATH, "//p[@class='product-card-name']")
    precios = driver.find_elements(By.XPATH, "//span[@class='prices-main-price']")
    enlaces = driver.find_elements(By.XPATH, "//a[@class='product-card text-black hover:no-underline ']")
    imagenes = driver.find_elements(By.XPATH, "//img[@class='lazy-image']")

    for nombre, precio, enlace, imagen in zip(nombres, precios, enlaces, imagenes):
        nombre_texto = nombre.text
        precio_texto = precio.text.strip()  # Mantén el formato con el símbolo $
        enlace_texto = enlace.get_attribute("href")
        imagen_url = imagen.get_attribute('src')
        if not imagen_url or imagen_url.endswith('blank.gif'):
            imagen_url = imagen.get_attribute('data-src')
        
        productos.append({
            "nombre": nombre_texto,
            "precio": precio_texto,
            "enlace": enlace_texto,
            "imagen_url": imagen_url
        })

numPagina = 1

while True:
    url = f"https://www.santaisabel.cl/desayuno/cereales-avenas-y-barras?page={numPagina}"
    driver.get(url)
    sleep(6)  # Espera a que cargue todo
    scrapeo()

    if numPagina == 5:
        break

    numPagina += 1

# Guardar en archivo JSON con el formato solicitado
with open("productosSantaIsabel.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=2)

# Guardar en la base de datos
db = SessionLocal()
for producto in productos:
    try:
        nuevo = Producto(
            nombre=producto["nombre"],
            precio=float(producto["precio"].replace("$", "").replace(".", "").replace(",", ".")),
            enlace=producto["enlace"],
            supermercado="Santa Isabel",
            imagen_url=producto["imagen_url"]
        )
        db.add(nuevo)
    except Exception as e:
        print(f"Error al agregar producto: {producto['nombre']}. Error: {e}")
db.commit()
db.close()

driver.quit()

print("Datos guardados en productosSantaIsabel.json")
print("Productos Santa Isabel guardados en MySQL")
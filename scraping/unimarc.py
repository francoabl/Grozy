from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Conexión a MySQL
from db import SessionLocal, Producto

# Configurar Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Opcional: para no abrir ventana
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

productos = []

# Ir a la primera página manualmente
driver.get("https://www.unimarc.cl/category/desayuno-y-dulces/cereales?page=1")
sleep(5)

# Función de scrapeo
def scrapeo():
    nombres = driver.find_elements(By.XPATH, "//p[contains(@class, 'Shelf_nameProduct')]")
    precios = driver.find_elements(By.XPATH, "//p[contains(@class, 'Text_text--primary')]")
    imagenes = driver.find_elements(By.XPATH, "//img[contains(@class, 'Shelf_defaultImgStyle')]")
    
    enlaces = []
    index = 1
    while True:
        try:
            enlace_xpath = f"/html/body/div[1]/div/main/div/section/div/div/div[{index}]/section/div[3]/div/div[3]/div[1]/div[2]/a"
            enlace = driver.find_element(By.XPATH, enlace_xpath)
            enlaces.append(enlace.get_attribute("href"))  # Obtén el href aquí
            index += 1
        except Exception:
            break

    # Ahora 'enlaces' es una lista de strings (hrefs), no de elementos
    for nombre, precio, imagen, enlace_url in zip(nombres, precios, imagenes, enlaces):
        nombre_texto = nombre.text.strip()
        precio_texto = precio.text.replace("$", "").replace(".", "").strip()
        imagen_url = imagen.get_attribute('src')
        productos.append({
            "nombre": nombre_texto,
            "precio": precio_texto,
            "enlace": enlace_url,
            "imagen_url": imagen_url
        })
        print(f"Nombre: {nombre_texto} - Precio: {precio_texto} - Imagen: {imagen_url} - Enlace: {enlace_url}")

# Función para cambiar de página haciendo clic
def cambiar_pagina(pagina):
    try:
        boton = driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div/div[4]/div/div/div[2]/div/a[{pagina}]")
        boton.click()
        sleep(8)
        return True
    except Exception as e:
        print(f"No se pudo cambiar a la página {pagina}: {e}")
        return False

# Iterar sobre varias páginas
pagina = 2  # Empieza en la página 2 (la 1 ya se cargó al inicio)
scrapeo()  # Scrapea la página 1

while True:
    if cambiar_pagina(pagina):
        scrapeo()
        pagina += 1
    else:
        break  # Si no puede cambiar, termina el bucle

driver.quit()

# Guardar en JSON
with open('productos_unimarc.json', 'w', encoding='utf-8') as f:
    json.dump(productos, f, ensure_ascii=False, indent=4)

# Guardar en MySQL
db = SessionLocal()
for producto in productos:
    # Limpia el precio y trata de convertirlo a float
    precio_limpio = producto["precio"].replace("$", "").replace(".", "").replace(",", ".").strip()
    try:
        precio_num = float(precio_limpio)
    except ValueError:
        print(f"⚠️ Precio inválido '{producto['precio']}' – se guarda como 0.0")
        precio_num = 0.0

    try:
        nuevo = Producto(
            nombre=producto["nombre"],
            precio=precio_num,
            enlace=producto["enlace"],
            supermercado="Unimarc",
            imagen_url=producto["imagen_url"]
        )
        db.add(nuevo)
    except Exception as e:
        print(f"❌ Error guardando producto en base de datos: {e}")
db.commit()
db.close()

print("✅ Productos guardados en productos_unimarc.json y en la base de datos MySQL")

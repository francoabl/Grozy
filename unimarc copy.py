import csv
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Configurar Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Opcional: no abre ventana
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL del sitio
url = 'https://www.unimarc.cl/category/desayuno-y-dulces/cereales?&page=1'
driver.get(url)
sleep(5)  # Espera a que cargue todo

productos = []

def scrapeo():
    nombres = driver.find_elements(By.XPATH, "//p[@class='Text_text__cB7NM Shelf_nameProduct__CXI5M Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--regular__KSs6J Text_text--md__H7JI_ Text_text--black__zYYxI Text_text__cursor--pointer__WZsQE Text_text--none__zez2n']")
    precios = driver.find_elements(By.XPATH, "//p[@class='Text_text__cB7NM Text_text--left__1v2Xw Text_text--flex__F7yuI Text_text--medium__rIScp Text_text--lg__GZWsa Text_text--primary__OoK0C Text_text__cursor--auto__cMaN1 Text_text--none__zez2n']")
    imagenes = driver.find_elements(By.XPATH, "//img[@class='Shelf_defaultImgStyle__ylyx2']")
    enlaces = driver.find_elements(By.XPATH, "//div[contains(@class, 'Shelf_productCard__')]//a[@class='ProductCard_productCard__link__wQKkT']")
    
    for nombre, precio, imagen, enlace in zip(nombres, precios, imagenes, enlaces):
        nombre_texto = nombre.text.strip()
        precio_texto = precio.text.replace("$", "").replace(".", "").strip()
        imagen_url = imagen.get_attribute('src')
        enlace_url = enlace.get_attribute('href')
        productos.append({
            "nombre": nombre_texto,
            "precio": precio_texto,
            "imagen_url": imagen_url,
            "enlace": enlace_url
        })
        print(f"Nombre: {nombre_texto} - Precio: {precio_texto} - Imagen: {imagen_url} - Enlace: {enlace_url}")

sleep(8)  # Espera inicial para cargar todo
scrapeo()

for i in range(2, 5):  # Desde la página 2 hasta la 4
    sleep(3)
    click = driver.find_element(By.XPATH, f"/html/body/div[1]/div/main/div/div[4]/div/div/div[2]/div/a[{i}]")
    click.click()
    sleep(5)
    scrapeo()

# Guardar en archivo JSON
with open("productosUnimarc.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=2)

# Guardar en archivo CSV
with open("productosUnimarc.csv", "w", encoding="utf-8", newline='') as archivo_csv:
    writer = csv.DictWriter(archivo_csv, fieldnames=["nombre", "precio", "imagen_url", "enlace"])
    writer.writeheader()
    writer.writerows(productos)

driver.quit()

print("Datos guardados en productosUnimarc.json y productosUnimarc.csv")
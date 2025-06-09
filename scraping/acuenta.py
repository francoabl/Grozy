import csv
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Selenium
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Opcional: no abre ventana
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL del sitio
url = 'https://www.acuenta.cl/ca/desayuno-y-dulces/cereales-avenas-y-barras/44/4403'
driver.get(url)
sleep(5)  # Espera a que cargue todo

# Extraer elementos
nombres = driver.find_elements(By.XPATH, "//p[@class='CardName__CardNameStyles-sc-147zxke-0 eriwcz prod__name']")
precios = driver.find_elements(By.XPATH, "//p[@class='styles__PumStyles-sc-omx4ld-0 CardPum__CardPumStyles-sc-1vz27ac-0 dFNFqr MlrBO']")

# Guardar datos
productos = {}



for nombre, precio in zip(nombres, precios):
    nombre_texto = nombre.text.strip()
    precio_texto = precio.text.strip()
    productos[nombre_texto] = precio_texto
    print(f"Nombre: {nombre_texto} - Precio: {precio_texto}")

with open("productosAcuenta.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=2)



with open("productosAcuenta.csv", "w", encoding="utf-8", newline='') as archivo_csv:
    writer = csv.DictWriter(archivo_csv, fieldnames=["nombre", "precio"])
    writer.writeheader()
    # Convertir productos a una lista de diccionarios
    writer.writerows([
        {"nombre": nombre, "precio": precio}
        for nombre, precio in productos.items()
    ])

driver.quit()
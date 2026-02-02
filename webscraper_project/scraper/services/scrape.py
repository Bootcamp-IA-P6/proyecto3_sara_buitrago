from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# Para Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Para Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def scrape_website():
    # Configurar directorio para screenshots - Usar ruta absoluta al volumen
    screenshots_dir = "/app/screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    # Configurar Selenium
    options = Options()
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--no-sandbox')  # Requerido para algunos servidores
    options.add_argument('--disable-dev-shm-usage')  # Para evitar errores de memoria
    
    # Añadimos un user-agent para parecer un navegador real y evitar detecciones
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0")

    # 🔹 Aquí inicializamos correctamente `service` PARA CHROME
    #service = Service(ChromeDriverManager().install())

    # Para Chrome
    # Selenium Manager se encargará de descargar y gestionar el WebDriver
    #service = Service()  # No es necesario especificar el ejecutable
    #driver = webdriver.Chrome(service=service, options=options)
    
    # Configurar el servicio de GeckoDriver - FIREFOX
    service = Service("/usr/local/bin/geckodriver")
    # Crear el WebDriver de Firefox
    driver = webdriver.Firefox(service=service, options=options)

    wait = WebDriverWait(driver, 20)
    
    # Navegar al sitio web
    url = "https://www.pccomponentes.com/portatiles/nuevo/para-profesionales?seller=pccomponentes"
    driver.get(url)
    print(driver.title)
    
    # <--  Aceptar las cookies  -->
    try:
        print("Buscando botón de cookies...")
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, "cookiesAcceptAll"))
        )
        accept_button.click()
        print("¡Cookies aceptadas!")
        
        time.sleep(2) 
    except Exception as e:
        print("No se encontró el popup de cookies, continuando...")
        
    
    
    # CAPTURA DE PANTALLA - DEBUG
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(screenshots_dir, f"captura_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Captura de pantalla guardada en: {screenshot_path}")
   
    #busqueda anterior con chrome:
    #products = driver.find_elements(By.CSS_SELECTOR, "div.product-card")
    
    # buscar productos (FIREFOX+DOCKER):
    products = driver.find_elements(By.CSS_SELECTOR, "div.product-card")
    ofertas = []  


    for product in products:
        try:
            # Creamos una espera específica para CADA producto.
            product_wait = WebDriverWait(product, 5)
            
            badge_descuento = product.find_elements(By.CSS_SELECTOR, ".discount-badge") 
            
            descuento_valor = 0
            if badge_descuento:
                texto_dto = badge_descuento[0].text 
                descuento_valor = int(texto_dto.replace("-", "").replace("%", "").strip())
            
            if descuento_valor > 10:
                try:
                    #OPCION CHROME SIN DOCKER:
                    #nombre_el = product.find_element(By.CSS_SELECTOR, '[data-e2e="title-card"]')
                    #OPCION CHROME SIN DOCKER:
                    #precio_el = product.find_element(By.CSS_SELECTOR, '[data-e2e="price-card"]')
                    
                    name = product.find_element(By.CSS_SELECTOR, '[data-e2e="title-card"]').text.strip()
                    precio_texto = product.find_element(By.CSS_SELECTOR, '[data-e2e="price-card"]').text.replace("€", "").replace(".", "").replace(",", ".").strip()
                    precio_final = float(precio_texto)

                    print(f"✅ ¡OFERTA! {name} - Antes era más caro, ahora: {precio_final}€")
                    ofertas.append({
                    "name": name,
                    "price": precio_final,
                    "discount": descuento_valor
                    })
                    
                except Exception as e:
                    print(f"No se pudo extraer detalle del producto: {e}")   

        except Exception:
            print(f"Error procesando un producto: {e}")
            continue
    

    
    driver.quit()
    return ofertas
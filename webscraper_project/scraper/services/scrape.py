from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Para Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_website():
    # Configurar Selenium
    options = Options()
    #options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--no-sandbox')  # Requerido para algunos servidores
    options.add_argument('--disable-dev-shm-usage')  # Para evitar errores de memoria

    # 🔹 Aquí inicializamos correctamente `service`
    service = Service(ChromeDriverManager().install())

    # Para Chrome
    # Selenium Manager se encargará de descargar y gestionar el WebDriver
    #service = Service()  # No es necesario especificar el ejecutable
    driver = webdriver.Chrome(service=service, options=options)

    # Navegar al sitio web
    url = "https://www.pccomponentes.com/portatiles/nuevo/para-profesionales?seller=pccomponentes"
    driver.get(url)
    print(driver.title)
    time.sleep(5)
    
    products = driver.find_elements(By.CSS_SELECTOR, "div.product-card")
    ofertas = []  


    for product in products:
        try:
            
            badge_descuento = product.find_elements(By.CSS_SELECTOR, ".discount-badge") 
            
            descuento_valor = 0
            if badge_descuento:
                # Como solo hay uno (o el primero es el que vale), accedemos al índice [0]
                texto_dto = badge_descuento[0].text  # Esto te dará "-18%"
    
                descuento_valor = int(texto_dto.replace("-", "").replace("%", "").strip())
            
            if descuento_valor > 10:
                try:
                    
                    nombre_el = product.find_element(By.CSS_SELECTOR, '[data-e2e="title-card"]')
                    name = nombre_el.text.strip()

                    precio_el = product.find_element(By.CSS_SELECTOR, '[data-e2e="price-card"]')
                    
                    precio_texto = precio_el.text.replace("€", "").replace(".", "").strip()
                    precio_final = float(precio_texto)

                    print(f"✅ ¡OFERTA! {name} - Antes era más caro, ahora: {precio_final}€")

                    # Aquí ya podrías hacer el ScrapedDataEdit.objects.create(...)
                    
                except Exception as e:
                    print(f"No se pudo extraer detalle del producto: {e}")   

                
                ofertas.append({
                    "name": name,
                    "price": precio_final,
                    "discount": descuento_valor
                })

        except Exception:
            continue
    

    
    driver.quit()
    return ofertas
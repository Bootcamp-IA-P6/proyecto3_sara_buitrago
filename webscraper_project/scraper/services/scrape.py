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
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--no-sandbox')  # Requerido para algunos servidores
    options.add_argument('--disable-dev-shm-usage')  # Para evitar errores de memoria
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # 🔹 Aquí inicializamos correctamente `service`
    service = Service(ChromeDriverManager().install())

    # Para Chrome
    # Selenium Manager se encargará de descargar y gestionar el WebDriver
    #service = Service()  # No es necesario especificar el ejecutable
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 15)
    
    # Navegar al sitio web
    url = "https://www.pccomponentes.com/portatiles/nuevo/para-profesionales?seller=pccomponentes"
    driver.get(url)
    print(driver.title)
    time.sleep(5)
    
    try:
        print("Buscando botón de cookies...")
        # Usamos el mismo selector que funcionó en Docker
        accept_button = wait.until(
            EC.element_to_be_clickable((By.ID, "cookiesAcceptAll"))
        )
        accept_button.click()
        print("¡Cookies aceptadas!")
        time.sleep(2) # Pequeña pausa para que la página se recargue
    except Exception as e:
        print(f"No se encontró el popup de cookies, continuando... {e}")
    
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
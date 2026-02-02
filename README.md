# PcComponentes Scraper (Local Version)

Este proyecto es un web scraper diseñado para extraer ofertas de portátiles de la web de PcComponentes. Esta versión está configurada para ejecutarse directamente en tu máquina local utilizando Python, Django y Selenium.

## Descripción

El scraper realiza las siguientes tareas:

1.  Inicia un navegador Chrome en modo headless (sin interfaz gráfica).
2.  Utiliza opciones específicas para evitar la detección por parte de sistemas de seguridad como Cloudflare.
3.  Navega a la URL de portátiles para profesionales de PcComponentes.
4.  Acepta automáticamente el banner de cookies si aparece.
5.  Filtra los productos que tienen un descuento superior al 10%.
6.  Extrae el nombre, el precio y el porcentaje de descuento de cada oferta.
7.  Guarda esta información en una base de datos SQLite a través de un modelo de Django.

## Prerrequisitos

Asegúrate de tener instalado Python 3 y pip en tu sistema. Se recomienda encarecidamente utilizar un entorno virtual.

## Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el scraper en tu máquina local:

1.  **Clona el repositorio:**

    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Crea y activa un entorno virtual:**

    ```bash
    # Para Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplica las migraciones de la base de datos:**
    Este comando crea el archivo `db.sqlite3` y las tablas necesarias en el directorio `webscraper_project`.
    ```bash
    python webscraper_project/manage.py migrate
    ```

## Ejecución

Para iniciar el proceso de scraping, ejecuta el siguiente comando desde la raíz del proyecto (con el entorno virtual activado):

```bash
python webscraper_project/manage.py scraper
```

El scraper comenzará a ejecutarse y mostrará en la consola las ofertas que vaya encontrando.

## Cómo Funciona

### Manejo de la Detección de Bots

Al ejecutarse en modo headless, el navegador puede ser detectado por sistemas como Cloudflare, que muestran una página de verificación ("Attention Required!"). Para evitar esto, el script `scrape.py` configura las opciones de Chrome con los siguientes argumentos:

```python
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--user-agent=...")
```

Estas opciones ayudan a que el navegador automatizado se parezca más a uno controlado por un humano.

### Estructura del Proyecto

```
.
├── requirements.txt       # Dependencias de Python.
├── scraper/               # Aplicación de Django.
│   ├── management/commands/
│   │   └── scraper.py    # Comando de gestión que llama a la lógica de scraping.
│   ├── models.py          # Definición del modelo de datos (ScrapedDataEdit).
│   └── ...
├── scrape.py              # Archivo con la función principal de Selenium.
└── webscraper_project/    # Directorio del proyecto Django.
    ├── db.sqlite3         # Base de datos SQLite (se genera aquí).
    └── ...
```

## Ver los Datos

Una vez que el script ha terminado su ejecución, los datos extraídos se guardan en el archivo `webscraper_project/db.sqlite3`.

Para inspeccionar los datos, puedes usar una herramienta gráfica como [DB Browser for SQLite](https://sqlitebrowser.org/).

1.  Abre `DB Browser for SQLite`.
2.  Selecciona "Abrir Base de Datos" y navega hasta tu archivo `webscraper_project/db.sqlite3`.
3.  Ve a la pestaña "Examinar Datos" y selecciona la tabla correspondiente (probablemente `scraper_scrapeddataedit`).

## Solución de Problemas

- **Error "Attention Required! | Cloudflare"**: Esto significa que el script ha sido detectado como un bot. Asegúrate de que las opciones de Chrome en `scrape.py` (sección "Manejo de la Detección de Bots") están presentes y son correctas. Si el problema persiste, es posible que Cloudflare haya actualizado sus mecanismos de detección.
- **El scraper no encuentra productos**: Si PcComponentes cambia la estructura de su web, los selectores de CSS en `scrape.py` podrían dejar de funcionar. Los errores en la consola indicarán qué elemento no se pudo encontrar.

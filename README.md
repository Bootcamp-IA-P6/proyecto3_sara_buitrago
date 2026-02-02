# PcComponentes Scraper con Capturas de Pantalla

Este proyecto es un web scraper automatizado diseñado para extraer ofertas de portátiles de la web de PcComponentes. Utiliza Django para la gestión de datos y Selenium para la automatización del navegador, todo ejecutado dentro de un contenedor Docker. Esta versión incluye una funcionalidad para tomar capturas de pantalla durante el proceso, lo que facilita la depuración.

## Descripción

El scraper realiza las siguientes tareas:

1.  Inicia un navegador Firefox en modo headless (sin interfaz gráfica).
2.  Navega a la URL de portátiles para profesionales de PcComponentes.
3.  Acepta automáticamente el banner de cookies para poder acceder al contenido.
4.  **Toma una captura de pantalla de la página completa después de cargarla.**
5.  Filtra los productos que tienen un descuento superior al 10%.
6.  Extrae el nombre, el precio y el porcentaje de descuento de cada oferta.
7.  Guarda esta información en una base de datos SQLite a través de un modelo de Django.

## Prerrequisitos

Asegúrate de tener instalados los siguientes programas en tu sistema:

- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Instalación y Puesta en Marcha

Sigue estos pasos para clonar el repositorio y ejecutar el scraper:

1.  **Clona el repositorio:**

    ```bash
    git clone <URL-del-repositorio>
    cd <nombre-del-directorio>
    ```

2.  **Construye la imagen de Docker:**
    Este comando lee el `Dockerfile` y crea la imagen del contenedor con todas las dependencias necesarias (Python, Firefox, Selenium, etc.).

    ```bash
    docker compose build
    ```

3.  **Ejecuta el contenedor:**
    Este comando inicia el contenedor. El scraper se ejecutará automáticamente, guardará los datos y las capturas, y el contenedor se detendrá.
    ```bash
    docker compose up -d
    ```

## Cómo Funciona

### Dockerfile

El `Dockerfile` define los pasos para crear la imagen del contenedor:

- Instala dependencias del sistema necesarias para Firefox.
- Descarga e instala `geckodriver`.
- **Crea un directorio `/app/screenshots` dentro del contenedor para almacenar las capturas.**
- Copia el código del proyecto y los requisitos de Python.
- Define el comando por defecto que se ejecutará al iniciar el contenedor.

### Docker Compose

El archivo `docker-compose.yml` orquesta el servicio:

- **`build: .`**: Indica que la imagen se debe construir desde el `Dockerfile`.
- **`ports: - 8000:8000`**: Mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina.
- **`volumes:`**: Define las carpetas compartidas entre tu máquina y el contenedor.
  - **`.:/app`**: Monta tu directorio local en `/app` para persistir la base de datos.
  - **`./screenshots:/app/screenshots`**: **Mapea la carpeta local `./screenshots` a la carpeta del contenedor `/app/screenshots`**. Esto permite que las capturas de pantalla se guarden directamente en tu máquina.

### Lógica de Capturas de Pantalla

El script `scrape.py` está configurado para guardar las capturas en la ruta `/app/screenshots`. Aunque esta ruta es interna al contenedor, gracias al mapeo de volúmenes, los archivos aparecen en tu carpeta local `./screenshots/`. El nombre de cada captura incluye un timestamp para evitar que se sobrescriban.

## Ver los Datos

Una vez que el contenedor ha terminado su ejecución, los datos extraídos se guardan en dos lugares:

### Base de Datos

Los datos estructurados se guardan en el archivo `webscraper_project/db.sqlite3`. Puedes inspeccionarlos con una herramienta como [DB Browser for SQLite](https://sqlitebrowser.org/).

### Capturas de Pantalla

Las capturas de pantalla se guardan en la carpeta `screenshots/` en la raíz de tu proyecto. Puedes verlas directamente desde tu explorador de archivos o listarlas con la terminal:

```bash
ls screenshots/
```

## Estructura del Proyecto

```
.
├── docker-compose.yml      # Configuración de Docker Compose.
├── Dockerfile             # Definición de la imagen de Docker.
├── requirements.txt       # Dependencias de Python.
├── screenshots/           # Directorio para las capturas de pantalla (se crea automáticamente).
├── scraper/               # Aplicación de Django.
│   ├── management/commands/
│   │   └── scraper.py    # Comando de gestión con la lógica de Selenium y capturas.
│   ├── models.py          # Definición del modelo de datos.
│   └── ...
└── webscraper_project/    # Directorio del proyecto Django.
    ├── db.sqlite3         # Base de datos SQLite.
    └── ...
```

## Solución de Problemas

- **No se generan las capturas de pantalla:** Asegúrate de que la línea `volumes: - ./screenshots:/app/screenshots` está presente y es correcta en tu `docker-compose.yml`. Verifica también que la carpeta `screenshots/` exista en tu proyecto local (Docker la creará si no existe, pero es bueno comprobarlo).

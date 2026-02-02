# PcComponentes Scraper

Este proyecto es un web scraper automatizado diseñado para extraer ofertas de portátiles de la web de PcComponentes. Utiliza Django para la gestión de datos y Selenium para la automatización del navegador, todo ejecutado dentro de un contenedor Docker para garantizar un entorno consistente y replicable.

## Descripción

El scraper realiza las siguientes tareas:

1.  Inicia un navegador Firefox en modo headless (sin interfaz gráfica).
2.  Navega a la URL de portátiles para profesionales de PcComponentes.
3.  Acepta automáticamente el banner de cookies para poder acceder al contenido.
4.  Filtra los productos que tienen un descuento superior al 10%.
5.  Extrae el nombre, el precio y el porcentaje de descuento de cada oferta.
6.  Guarda esta información en una base de datos SQLite a través de un modelo de Django.

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
    Este comando inicia el contenedor. El scraper se ejecutará automáticamente, guardará los datos y el contenedor se detendrá.
    ```bash
    docker compose up -d
    ```

## Cómo Funciona

### Dockerfile

El `Dockerfile` define los pasos para crear la imagen del contenedor:

- Instala dependencias del sistema necesarias para Firefox.
- Descarga e instala `geckodriver`, el driver para Selenium.
- Copia el código del proyecto y los requisitos de Python.
- Define el comando por defecto que se ejecutará al iniciar el contenedor.

### Docker Compose

El archivo `docker-compose.yml` orquesta el servicio:

- **`build: .`**: Indica que la imagen se debe construir desde el `Dockerfile` en el directorio actual.
- **`ports: - 8000:8000`**: Mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina (útil si se quisiera ejecutar un servidor de desarrollo).
- **`volumes: - .:/app`**: Esta es la parte crucial. Monta el directorio actual de tu máquina (`.`) en el directorio `/app` del contenedor. Esto permite que los cambios en el código se reflejen en el contenedor y, lo más importante, que la base de datos SQLite (`db.sqlite3`) se guarde de forma persistente en tu máquina local.

### Comando de Ejecución

El comando definido en el `Dockerfile` es:

```sh
sh -c "python3 webscraper_project/manage.py migrate && python3 webscraper_project/manage.py scraper"
```

- `python3 manage.py migrate`: Aplica las migraciones de Django a la base de datos para crear las tablas necesarias. No borra datos existentes.
- `python3 manage.py scraper`: Ejecuta el comando de gestión personalizado `scraper`, que contiene la lógica de scraping.

## Ver los Datos

Una vez que el contenedor ha terminado su ejecución, los datos extraídos se guardan en el archivo `webscraper_project/db.sqlite3` en la raíz de tu proyecto.

Para inspeccionar los datos, puedes usar una herramienta gráfica como [DB Browser for SQLite](https://sqlitebrowser.org/).

1.  Abre `DB Browser for SQLite`.
2.  Selecciona "Abrir Base de Datos" y navega hasta tu archivo `webscraper_project/db.sqlite3`.
3.  Ve a la pestaña "Examinar Datos" y selecciona la tabla correspondiente (probablemente se llame `nombreapp_scrapeddataedit`).

## Estructura del Proyecto

```
.
├── docker-compose.yml      # Configuración de Docker Compose.
├── Dockerfile             # Definición de la imagen de Docker.
├── requirements.txt       # Dependencias de Python.
├── scraper/               # Aplicación de Django.
│   ├── management/commands/
│   │   └── scraper.py    # Comando de gestión con la lógica de Selenium.
│   ├── models.py          # Definición del modelo de datos (ScrapedDataEdit).
│   └── ...
└── webscraper_project/    # Directorio del proyecto Django.
    ├── db.sqlite3         # Base de datos SQLite (se genera aquí).
    └── ...
```

## Solución de Problemas

- **El contenedor se apaga solo:** Esto es el comportamiento esperado. El contenedor está diseñado para ejecutar una única tarea (el scraping) y luego detenerse. No es un servidor que debe permanecer activo.

- **El scraper falla:** Si PcComponentes cambia la estructura de su web, los selectores de CSS en `scraper.py` podrían dejar de funcionar. Los logs del contenedor (`docker compose logs server-1`) darán pistas sobre qué elemento no se pudo encontrar.

# SIWEB

Aplicación web para la consulta y visualización de terremotos filtrados por fecha, latitud, longitud y magnitud, con resultados paginados y visualización en mapa.

## Requisitos

- Python 3.10 o superior
- pip
- Virtualenv (opcional pero recomendado)
- PostgreSQL o SQLite (según configuración de tu proyecto)
- Node.js y npm (solo si usas herramientas frontend adicionales)

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/inncubux/SIWEB.git
   cd SIWEB
   ```

2. **Crea y activa un entorno virtual:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Edita `config/settings.py` para ajustar la configuración de la base de datos si es necesario.

5. **Aplica las migraciones:**
   ```sh
   python manage.py migrate
   ```

6. **Carga datos de ejemplo (opcional):**
   ```sh
   python manage.py loaddata datos_ejemplo.json
   ```

7. **Inicia el servidor de desarrollo:**
   ```sh
   python manage.py runserver
   ```

8. **Accede a la aplicación:**
   - Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Uso

- Filtra terremotos por fecha, latitud, longitud y magnitud.
- Visualiza los resultados en una tabla paginada y en un mapa interactivo.
- Haz clic en los puntos del mapa para ver detalles del evento.

## Notas

- Asegúrate de tener los modelos y migraciones correctamente configurados.
- Si usas otra base de datos, revisa la configuración en `settings.py`.
- Si tienes problemas con dependencias, revisa el archivo `requirements.txt`.

## Contacto

Para dudas o soporte, contacta a: [axel.mondaca@alumnos.ucn.cl]
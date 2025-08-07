# API Django y Django Rest Framework

La API desarrollada en Django y Django Rest Framework (DRF) actúa como el motor detrás del *Mapa de establecimientos
educativos y productivos*, proporcionando datos esenciales y funcionalidades clave para la visualización y exploración
del mapa de establecimientos educativos y productivos. Esta API está diseñada para interactuar eficientemente con la
aplicación frontend y gestionar datos geoespaciales almacenados en PostgreSQL con la extensión PostGIS.

## Requisitos Previos

- Python 3.10
- Pip
- Virtualenv (recomendado)

## Configuración del Proyecto

#### Crear variables de entorno:

Copiar el archivo .env.example a .env y configurar las variables de entorno necesarias.

#### Configuración de la Clave Secreta:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copia el resultado obtenido dentro del archivo .env como valor de `DJANGO_SECRET_KEY`.


## Despliegue en un Servidor Linux

### Preparación del Servidor:

Asegúrate de que el servidor tenga instalado Python 3.10 y pip. Puedes usar apt o yum según la distribución.

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### Clonar el Repositorio

```bash
git clone https://github.com/MathiasJF19/backend_mapa_oei.git
cd backend_mapa_oei
```

### Configuración del Entorno Virtual (Opcional, pero recomendado)

```bash
# Crear un entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt
```

### Desarrollo
Para ejecutar el proyecto en modo desarrollo, ejecutar:

```bash
python manage.py migrate
python manage.py createcachetable 
python manage.py runserver
```
La aplicación estará disponible en http://localhost:8000/.

### Producción

#### Migraciones y Colección Estática:

Ejecuta las migraciones y reúne los archivos estáticos.

```bash
python manage.py migrate
python manage.py createcachetable 
python manage.py collectstatic
```

### Configuración del Servicio:

Configura el servicio Django para su ejecución en producción. Consulta la documentación de Django para obtener más
detalles.

### Restaurar la Base de Datos PostgreSQL

Para realizar un restore de la base de datos PostgreSQL, sigue estos pasos:

Antes de realizar un restore, asegúrate de tener la copia de seguridad de la base de datos actual.
Reemplaza `base_de_datos` con el nombre real de tu base de datos y `backup.sql` con la ubicación donde se encuentra
el archivo de respaldo.

```bash
psql -U nombre_de_usuario -d base_de_datos -f backup.sql
```

#### Aplicar Migraciones de Django:

Después de restaurar la base de datos, es posible que necesites aplicar las migraciones de Django para asegurarte de que
la estructura de la base de datos coincida con la versión actual de tu aplicación.

```bash
python manage.py migrate
```

### Arrancar el Servicio:

Ejecuta el servicio Django en modo producción. Puedes utilizar Gunicorn, uWSGI u otro servidor WSGI.

```bash
gunicorn config.wsgi:application --workers 4 -b 127.0.0.1:8000
```

### Configuración del Firewall: OPCIONAL

```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### Configuración del Proxy Inverso (Nginx): OPCIONAL

Configura el servidor web (Nginx) como proxy inverso para redirigir las solicitudes al servicio Django.

```nginx
server {
    listen 80;
    server_name domino.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /ruta/al/proyecto;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Asegúrate de ajustar domino.com y la ruta real al proyecto para encontrar los archivos estáticos.


### Configuración del Proxy Inverso (Apache): OPCIONAL

Configurar Apache para actuar como un proxy inverso que redirige las solicitudes de archivos estáticos al servidor Gunicorn/DRF y pasa el resto de las solicitudes a Django.

Ejemplo de configuración de Apache en el archivo de configuración httpd.conf:

```
<VirtualHost *:80>
    ServerName tu.dominio.com

    # Configuración para servir archivos estáticos
    Alias /static /ruta/a/tu/proyecto/static
    <Directory /ruta/a/tu/proyecto/static>
        Require all granted
    </Directory>

    # Configuración del proxy inverso para Gunicorn/DRF
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

Luego, reiniciar el servicio de systemd
```bash
sudo systemctl restart apache2
```


#### Reiniciar el Servidor Web:

Reinicia el servidor web para aplicar los cambios.

```bash
sudo service nginx restart
```

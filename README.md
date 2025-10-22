# Trabajo Práctico Integrador - Arquitectura y Sistemas Operativos

Este repositorio es parte del **TPI** para la materia **Arquitectura y Sistemas Operativos** de la **Tecnicatura Universitaria en Programacion a Distancia**, realizado por los integrantes **Pablo Vera (comisión 13)** y **Martin Vazquez (comisión 8)**. El objetivo es demostrar cómo diferentes aplicaciones ejecutandose en contedores pueden interactuar entre sí muy facil mente mediante el uso de **Docker Compose**.

## Descripción del Proyecto

El proyecto consta de tres aplicaciones:

1. **docker-app**: Una aplicación web realizada en Flask que renderiza una página HTML sobre Docker.
2. **virtualbox-app**: Otra aplicación web en Flask que renderiza una página HTML sobre VirtualBox.
3. **monitor-app**: Una aplicación en Python que monitorea las otras dos aplicaciones y muestra si están en ejecución o no.

### Características

- **docker-app** y **virtualbox-app** utilizan volúmenes para permitir modificar los archivos HTML y ver los cambios en tiempo real sin necesidad de reconstruir o reiniciar los contenedores.
- **monitor-app** verifica periódicamente el estado de las otras dos aplicaciones y expone un endpoint `/status` que muestra si están activas o no.

## Ventajas de Docker Compose

El uso de **Docker Compose** simplifica la orquestación de múltiples contenedores. En este proyecto, Docker Compose se utiliza para:

- Crear y configurar los contenedores de las tres aplicaciones.
- Definir una red compartida automáticamente para que los contenedores puedan comunicarse entre sí.
- Configurar variables de entorno y dependencias entre servicios.

### Comparación con `docker run`

Si hubiéramos utilizado `docker run` en lugar de Docker Compose, habría sido necesario:

1. Crear manualmente una red Docker:
```sh
docker network create my-network
```

2. Ejecutar manualmente cada contenedor y conectarlo a la red:
```sh
docker run --rm -d --name virtualbox-app --network my-network -p 5001:5000 -v $(pwd)/virtualbox-app:/app virtualbox-app
docker run --rm -d --name docker-app --network my-network -p 5002:5000 -v $(pwd)/docker-app:/app docker-app
docker run --rm -d --name monitor --network my-network -p 8000:5000 -e TARGETS=http://virtualbox-app:5000,http://docker-app:5000 -e INTERVAL=10 monitor-app
```
3. Gestionar manualmente las dependencias entre los contenedores.

Con Docker Compose, todo esto se define en un único archivo docker-compose.yml, lo que facilita la configuración y el despliegue.

## Cómo Ejecutar el Proyecto
1. Clona este repositorio
```sh
git clone [https://github.com/martinvzutn/ayso-tpi](https://github.com/martinvzutn/ayso-tpi)
cd ayso-tpi
```

2. Construye y ejecuta los servicios con Docker Compose:

```sh
docker-compose up -d
```

3. Accede a las aplicaciones
    - docker-app: http://localhost:5002
    - virtualbox-app: http://localhost:5001
    - monitor-app: http://localhost:8000/status

## Integrantes
- Vázquez, Martín (comisión 8)
- Vera, Pablo (comisión 13)




<hr>

## Aclaracion extra sobre los nombres nombres de servicio como si fueran nombres de host
En Docker Compose, los servicios definidos en el archivo docker-compose.yml se ejecutan dentro de una red Docker predeterminada (a menos que se especifique otra red). Dentro de esta red, los contenedores pueden comunicarse entre sí utilizando los nombres de servicio como si fueran nombres de host.

¿Cómo funciona?
Cuando se define un servicio en docker-compose.yml, como virtualbox-app o docker-app, Docker Compose automáticamente asigna un nombre de host al contenedor basado en el nombre del servicio. Esto significa que, en lugar de usar la dirección IP del contenedor (que puede cambiar), se puede puede referir al servicio directamente por su nombre.

Por ejemplo, en el archivo docker-compose.yml tenemos:

```yml
environment:  
    - TARGETS=http://virtualbox-app:5000,http://docker-app:5000
```
Aquí, monitor utiliza las URLs http://virtualbox-app:5000 y http://docker-app:5000 para comunicarse con los otros dos servicios. Docker resuelve automáticamente estos nombres (virtualbox-app y docker-app) al contenedor correspondiente dentro de la red.

Ventajas de usar nombres de servicio
1. Evita la dependencia de direcciones IP: Las direcciones IP de los contenedores pueden cambiar cada vez que se reinician. Usar nombres de servicio garantiza que siempre se pueda comunicar con el contenedor correcto.
2. Configuración más sencilla: No hay que preocuparse por crear y gestionar nombres de host o direcciones IP manualmente.
3. Compatibilidad con redes personalizadas: Si se definen redes personalizadas en Docker Compose, los nombres de servicio seguirán funcionando dentro de esas redes.
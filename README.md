# Bot de Discord Valorant News

Este es un bot de Discord que proporciona noticias sobre el juego Valorant de Riot Games. El bot consulta un sitio web de noticias y envía las últimas noticias a un canal de Discord específico cada 15 minutos. Para que funcione, es necesario tener el script alojado en una máquina local, ya que se ejecuta en segundo plano.

## Prerequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu entorno de desarrollo:

- Python 3.x: Puedes descargarlo desde [python.org](https://www.python.org/downloads/)
- Git: Puedes descargarlo desde [git-scm.com](https://git-scm.com/downloads)


## Instalación

Para instalar y ejecutar este bot localmente, sigue estos pasos:

1. Clona este repositorio en tu máquina local:

  ```git clone https://github.com/lucio-drDEV/bot-valorant-news.git  ```


2. Accede al directorio del repositorio:

  ```cd bot-valorant-news```

3. Crea un entorno virtual (opcional pero recomendado):

 ```python3 -m venv nombre_del_entorno_virtual```

4. Activa el entorno virtual:

- En Windows:

  ```nombre_del_entorno_virtual\Scripts\activate```


- En macOS y Linux:

  ```source nombre_del_entorno_virtual/bin/activate```

5. Instala las dependencias del proyecto desde `requirements.txt`:

  ```pip install -r requirements.txt```

## Uso

* Para ejecutar el bot, utiliza el siguiente comando:

  ```python3 bot_valo.py```

* Recuerda desactivar el entorno virtual cuando hayas terminado de usar el bot:

  ```deactivate```

## Contribuir

* Si quieres contribuir a este proyecto, sigue estos pasos:

1. Haz un fork de este repositorio.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request.

## Invitar al bot a tu servidor

Para invitar al bot a tu servidor de Discord, utiliza el siguiente enlace:

[Invitar al bot a tu servidor](https://discord.com/oauth2/authorize?client_id=1147753137877307433)

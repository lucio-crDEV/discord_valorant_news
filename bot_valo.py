import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from urllib.parse import urljoin
import asyncio

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar las intenciones del bot de Discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Configurar el bot de Discord con las intenciones
bot_token = os.getenv("DISCORD_TOKEN")
bot_prefix = "!"  # El prefijo que activará los comandos del bot
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Lista para almacenar las noticias ya enviadas
noticias_enviadas = set()

# Función para obtener las noticias
def obtener_noticias():
    url = "https://www.millenium.gg/juegos/juego-78/noticias"

    # Realizar una solicitud HTTP para obtener el contenido de la página
    response = requests.get(url)
    if response.status_code == 200:
        # Analizar el contenido HTML de la página con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encuentra todas las etiquetas <article> que contienen noticias
        articulos = soup.find_all("article")

        # Revertir la lista de artículos para mostrar las noticias más recientes al principio
        articulos.reverse()

        noticias = []
        for article in articulos:

            # Encontrar la etiqueta <a> dentro de <article> que contiene el título y la URL
            enlace = article.find("a", class_="c-article__link")

            # Verificar si se encontró la etiqueta <a>
            if enlace is not None:
                # Obtener el título de la noticia
                titulo = enlace.text.strip()

                # Obtener la URL del enlace (puede ser relativa, así que construye la URL completa)
                url_noticia = urljoin(url, enlace["href"])

                # Verificar si la URL de la noticia contiene "/tag/"
                if "/tag/" not in url_noticia:

                    # Agregar el título, la URL de la noticia y la URL de la imagen a la lista de noticias
                    noticias.append({"titulo": titulo, "url_noticia": url_noticia})
        return noticias
    else:
        return None

# Comando para obtener las noticias
@bot.command()
async def valorant_news(ctx):
    noticias = obtener_noticias()

    if noticias:
        # Enviar las noticias como mensajes en Discord
        for noticia in noticias:
            # Comprobar si la noticia ya fue enviada
            if noticia['url_noticia'] not in noticias_enviadas:
                # Construye el mensaje con el título, el vínculo y la miniatura de la noticia
                mensaje = f"**Título:** {noticia['titulo']}\n**Enlace:** {noticia['url_noticia']}"

                # Envía el mensaje en Discord
                await ctx.send(mensaje)

                # Agrega la URL de la noticia a la lista de noticias enviadas
                noticias_enviadas.add(noticia['url_noticia'])
    else:
        await ctx.send("No se pudieron obtener noticias en este momento.")

# Función para enviar noticias automáticamente cada 15 minutos
@tasks.loop(minutes=15)
async def enviar_noticias():
    noticias = obtener_noticias()
    canal_id = 1148220610468651112 # Reemplaza con la ID del canal
    canal = bot.get_channel(canal_id)

    if noticias and canal:
        for noticia in noticias:
            # Comprobar si la noticia ya fue enviada
            if noticia['url_noticia'] not in noticias_enviadas:
                mensaje = f"> [{noticia['titulo']}]({noticia['url_noticia']})"
                await canal.send(mensaje)

                # Agrega la URL de la noticia a la lista de noticias enviadas
                noticias_enviadas.add(noticia['url_noticia'])

# Iniciar el bot de Discord
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    enviar_noticias.start()  # Inicia el bucle para enviar noticias automáticamente

bot.run(bot_token)

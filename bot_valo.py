import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from urllib.parse import urljoin

# Cargar variables de entorno desde el archivo config.env
load_dotenv("config.env")

# Configurar el bot de Discord con las intenciones
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# URL de las noticias obtenida del archivo config.env
url_news = os.getenv("URL_NEWS")

# Lista para almacenar las noticias ya enviadas
noticias_enviadas = set()

# Función para obtener las noticias
def obtener_noticias():
    # Realizar una solicitud HTTP para obtener el contenido de la página
    response = requests.get(url_news)
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
                url_noticia = urljoin(url_news, enlace["href"])

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
    canal_id = os.getenv("CANAL_ID")  # ID del canal donde se enviarán las noticias
    canal = bot.get_channel(int(canal_id))

    if noticias and canal:
        for noticia in noticias:
            # Comprobar si la noticia ya fue enviada
            if noticia['url_noticia'] not in noticias_enviadas:
                mensaje = f"> [{noticia['titulo']}]({noticia['url_noticia']})"
                await canal.send(mensaje)

                # Agrega la URL de la noticia a la lista de noticias enviadas
                noticias_enviadas.add(noticia['url_noticia'])

# Comando para obtener las últimas noticias
@bot.command(name='actualizar')
async def actualizar_noticias(ctx):
    nuevas_noticias = obtener_noticias()
    
    if nuevas_noticias:
        # Verificar si hay nuevas noticias desde la última vez que se verificaron
        nuevas_noticias = [noticia for noticia in nuevas_noticias if noticia['url_noticia'] not in noticias_enviadas]
        
        if nuevas_noticias:
            # Enviar las nuevas noticias como mensajes en Discord
            for noticia in nuevas_noticias:
                mensaje = f"**Título:** {noticia['titulo']}\n**Enlace:** {noticia['url_noticia']}"
                await ctx.send(mensaje)

                # Agregar la URL de la noticia a la lista de noticias enviadas
                noticias_enviadas.add(noticia['url_noticia'])
                
            return
    await ctx.send("Las noticias están actualizadas.")
    
    
# Iniciar el bot de Discord
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print(f'Conectado a {len(bot.guilds)} servidores')
    
    # Obtener el objeto de canal
    canal_id = os.getenv("CANAL_ID")  # ID del canal donde se enviarán las noticias
    canal = bot.get_channel(int(canal_id))
    
    # Verificar si el canal se encontró
    if canal:
        print(f'Conectado al canal: {canal.name} (ID: {canal.id})')
        # Inicia el bucle para enviar noticias automáticamente
        enviar_noticias.start()
    else:
        print('El bot no se encontró en el servidor del canal especificado.')

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

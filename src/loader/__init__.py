import discord 
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import pathlib 
from pathlib import Path
import os
import sys
import asyncio
class EnvGetter():
    def __init__(self):
       self.__ENVFILE_PATH__ = Path(__file__).resolve().parent.parent.parent / ".env" # procurando - achando .env
       load_dotenv(dotenv_path=self.__ENVFILE_PATH__) # loading .env
       self.token = os.getenv("BOT_TOKEN")
       self.prefixo = os.getenv("BOT_PREFIX")
intents = discord.Intents.default()
intents.message_content = True
token = EnvGetter()
bot = commands.Bot(command_prefix=token.prefixo, intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")
    dots = 0
    try: 
        sync = await bot.tree.sync()
        print(f"Sincronizando {len(sync)} comandos de barra!")
    except Exception as e:
        print(f"Erro ao sincronizar: {e}")
async def load_extensions():
    CURRENT_DIR = Path(__file__).resolve().parent
    COGS_DIR = CURRENT_DIR.parent.parent / "cogs"
    BASE_DIR = COGS_DIR.parent

    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                cog_name = filename[:-3]
                module_path = f"cogs.{cog_name}"
                await bot.load_extension(module_path)
                print(f"Cog: {filename} carregado com sucesso como '{module_path}'")
            except Exception as e:
                print(f"Aconteceu um erro ao carregar o cog {filename}: {e}")
                continue

    



if __name__ == "__main__":
    print("Esse não é o arquivo certo a ser rodado.")
    sys.exit(1)

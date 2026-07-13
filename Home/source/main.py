"""
Arquivo principal. 
    Maneja o .env
        Cria o cliente do bot, 
        Carrega as extensões em cogs
        Executa o bot
"""
import discord
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from discord.ext import commands 
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX")
class Mybot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix=PREFIX, intents=intents)
    async def setup_hook(self) -> None:
        await load_extensions_from_dir(self)
        
        try: 
            sync = await self.tree.sync()
            print(f"Sincronizando {len(sync)} comandos de barra!")
        except Exception as e:
            print(f"Erro ao sincronizar comandos: {e}")
bot = Mybot()
@bot.event
async def on_ready() -> None:
    print(f"Bot online como {bot.user}")
async def load_extensions_from_dir(bot_instance) -> None:
    CURRENT_DIR = Path(__file__).resolve().parent 
    COGS_DIR = CURRENT_DIR.parent.parent / "cogs" 
    BASE_DIR = COGS_DIR.parent 
    
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR)) 
    if not COGS_DIR.exists():
        print(f"Erro: O diretório de cogs não foi encontrado em: {COGS_DIR}")
        return
    for filename in os.listdir(COGS_DIR): 
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                cog_name = filename[:-3]
                module_path = f"cogs.{cog_name}"
                await bot_instance.load_extension(module_path)
                print(f"Cog: {filename} carregado com sucesso como '{module_path}'")
            except Exception as e:
                print(f"Aconteceu um erro ao carregar o cog {filename}: {e}")
bot.run(TOKEN)


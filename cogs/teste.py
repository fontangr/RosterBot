import discord 
from discord.ext import commands 

class Teste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.hybrid_command(name="testar", description="ver se funciona")
    async def testar(self, ctx: commands.Context):
        if(ctx.interaction):
            await ctx.send("Ok.")
        else:
            await ctx.send("Por prefixo tá ok.")
    
async def setup(bot):
    await bot.add_cog(Teste(bot))

import discord
from discord.ext import commands
from discord import ui
from controllers.QueriesController import QueriesController


class SubstituicaoVagaModal(ui.Modal, title="Trocar Vaga"):
    vaga = ui.TextInput(
        label="Vaga: ",
        placeholder="Ex.: 'Sosuke Aizen'",
        required=True,
        min_length=8, 
        max_length=50 
    )
    universo = ui.TextInput(
        label="Universo: ",
        placeholder="Ex.: 'Bleach'",
        required=True,
        min_length=8,
        max_length=50
    )
    def __init__(self, controller: QueriesController):
        self.controller = controller
        self.interaction = discord.Interaction
    async def on_submit(self, interaction: discord.Interaction):
        resultado = self.controller.replace_vaga(
            discord_user_id=str(interaction.user.id),
            discord_guild_id=str(interaction.guild_id),
            vaga_substituicao=self.vaga.value,
            universo=self.universo.value
        )
        if resultado == 0:
            await interaction.response.send_message(
                f"Vaga modificada com sucesso!",
                 ephemeral=True
            )
        elif resultado == 1:
            await interaction.response.send_message(
                await "Ocorreu um erro internamente. Tente novamente!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("Parece que algo de errado não está certo! Um problema ocorreu e ele não deveria ocorrer...", ephemeral=True)

class SubsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):  
        self.bot = bot,
        self.controller = QueriesController()
    @commands.Context(name="alterar_vaga", description="muda uma vaga já existente para outra")
    async def alterar_vaga(self, ctx: commands.Context):
        if not self.controller.verificar_pessoa(
            discord_user_id=ctx.author.id,
            discord_guild_id=ctx.guild.id
        ):
            await ctx.reply("Você não tem uma vaga aqui no servidor para poder ser alterada! Se quiser se registrar, envie (`/registrar`)!")
            return 
        if ctx.interaction is None:
            await ctx.send(
                "Esse comando só funciona como slash command (`/alterar_vaga`). Não argumente. Também queria que fosse diferente."
            )
            return 
        await ctx.interaction.response.send_modal(SubstituicaoVagaModal(self.controller))
async def setup(bot: commands.Bot):
    await bot.add_cog(SubsCog(bot))
        
            
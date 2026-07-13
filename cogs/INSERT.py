import discord
from discord.ext import commands
from discord import ui
from controllers.QueriesController import QueriesController


class CadastroVagaModal(ui.Modal, title="Cadastrar Vaga"):
    vaga = ui.TextInput(
        label="Nome da vaga",
        placeholder="Ex: 'Sosuke Aizen'",
        required=True,
        max_length=50
    )   
    universo = ui.TextInput(
        label="Universo",
        placeholder="Ex.: 'Bleach'",
        required=True,
        min_length=8,
        max_length=50
    )
    def __init__(self, controller: QueriesController):
        super().__init__()
        self.controller = controller
        self.interaction = discord.Interaction
    async def on_submit(self, interaction: discord.Interaction):
        resultado = self.controller.set_vaga(
            vaga=self.vaga.value,
            discord_user=str(interaction.user),
            discord_user_id=str(interaction.user.id),
            discord_guild_id=str(interaction.guild_id),
            universo=self.universo.value
        )
        if resultado == 0:
            await interaction.response.send_message(
                f"Vaga '{self.vaga.value}' registrada com sucesso."
            )
        elif resultado == 1:
            await interaction.response.send_message(
                "Essa vaga já está ocupada nesse servidor!",
                ephemeral=True
            )
        elif resultado == 3: 
            await interaction.response.send_message(
                "O nome do personagem deve ter no máximo 2 palavras (nome e sobrenome). O texto aplicado é muito grande.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Ocorreu um erro internamente. Tente novamente!",
                ephemeral=True
            )


class CadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.controller = QueriesController()

    @commands.hybrid_command(name="registrar", description="Registra uma vaga")
    async def registrar(self, ctx: commands.Context):
        if self.controller.verificar_pessoa(
            discord_guild_id=ctx.guild.id,
            discord_user_id=ctx.author.id
        ):
            await ctx.reply("Você já tem uma vaga aqui!", ephemeral=True)
            return
        if ctx.interaction is None:
            await ctx.send(
                "Esse comando só funciona como slash command (`/registrar`). Não argumente. Também queria que fosse diferente."
            )
            return
        await ctx.interaction.response.send_modal(CadastroVagaModal(self.controller))

async def setup(bot: commands.Bot):
    await bot.add_cog(CadCog(bot))
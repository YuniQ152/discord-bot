import discord
from discord import Intents, ui, app_commands
from discord.ui import Select, View, Button, Modal
from discord.interactions import Interaction
from discord.ext import commands
from datetime import datetime

class ConfirmButton(View):
    def __init__(self):
        super().__init__(timeout=180)
        self.value = None
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: Button):
        self.value = True
        self.stop()
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: Interaction, button: Button):
        self.value = False
        self.stop()

class QotdModal(Modal, title="오늘의 질문"):
    with open("qotd.txt", "r", encoding="UTF8") as question_file:
        question = question_file.read()
    answer = ui.TextInput(label=f"{question}", style=discord.TextStyle.long, placeholder="여기에 입력하세요.", default="", max_length=1024, required=True)
    async def on_submit(self, interaction: Interaction):
        self.title, self.question, self.awnser = self.title, self.answer.label, self.answer
        await interaction.response.send_message(f"{interaction.user.mention}, 답변이 <#959548527762108436>에 기록되었습니다.", ephemeral=True)

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="qotd", description="오늘의 질문")
    async def qotd(self, interaction: discord.Interaction):
        modal = QotdModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.awnser:
            embed = discord.Embed(timestamp=datetime.now(), color=discord.Color.green())
            embed.add_field(name="[질문]", value=f"{modal.question}", inline=False)
            embed.add_field(name="[답변]", value=f"{modal.answer}", inline=False)
            embed.set_author(name=f"{interaction.user}님의 답변", icon_url=interaction.user.avatar)
            channel = self.bot.get_channel(959548527762108436)
            await channel.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot), guilds=[discord.Object(id=785849670092980225)])

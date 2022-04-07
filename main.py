import discord
from discord.ext import commands
import asyncio
import aiohttp
import os
from dotenv import load_dotenv


class Bot(commands.Bot):
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        await self.wait_until_ready()
        await bot.tree.sync(guild=discord.Object(id=785849670092980225))
        print(f"logged in as {self.user} (ID: {self.user.id})")
        print('------------')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
description = """A bot made by YuniQ"""
bot = Bot(command_prefix="!", description=description, intents=intents)


async def reload_cogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.unload_extension(f"cogs.{filename[:-3]}")
            await bot.load_extension(f"cogs.{filename[:-3]}")
    await bot.tree.sync(guild=discord.Object(id=785849670092980225))

@commands.has_role(802505359499067393)
@bot.command()
async def reload(ctx):
    await ctx.send("Reloading...")
    await reload_cogs()
    await ctx.send("Done")
@reload.error
async def reload_error(ctx):
    await ctx.send("권한이 없습니다.")

@commands.has_role(802505359499067393)
@bot.command()
async def setqotd(ctx, *, new_question):
    await ctx.send("Progressing...")
    with open("qotd.txt", "r", encoding="UTF8") as question_file:
        old_question = question_file.read()
    with open("qotd.txt", "w", encoding="UTF8") as question_file:
        question_file.write(new_question)
    channel = bot.get_channel(959548527762108436)
    embed = discord.Embed(title="오늘의 질문이 변경되었습니다.", color=discord.Color.yellow())
    embed.add_field(name="[새 질문]", value=f"{new_question}", inline=False)
    await channel.send(embed=embed)
    await reload_cogs()
    await ctx.send(f"Done.\n`{old_question}` → `{new_question}`")
@setqotd.error
async def setqotd_error(ctx):
    await ctx.send("권한이 없습니다.")

async def main():
    async with bot:
        load_dotenv('token.env')
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())
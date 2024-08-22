import os
import discord
from discord.ext import commands
import aiohttp
import json

from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CDC_URL = os.getenv("CDC_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


@bot.command()
async def a_cdc_esta_online(ctx):
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"client_key": CLIENT_KEY, "client_secret": CLIENT_SECRET})

    async with aiohttp.ClientSession() as session:
        async with session.post(CDC_URL, headers=headers, data=data) as response:
            if response.status < 404:
                await ctx.send("Sim, ela está online! ✨🙌💫")
            else:
                await ctx.send("Não, ela não está disponível. ⛔❌")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

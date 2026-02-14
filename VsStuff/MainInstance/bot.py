import discord
from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

prefix = ","

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Last line here

bot.run(DISCORD_TOKEN)
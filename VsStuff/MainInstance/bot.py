import os
import threading
import pathlib
import asyncio
from flask import Flask
from discord.ext import commands
from dotenv import load_dotenv
import discord

print("Starting bot from: " + __file__)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=',', help_command=None, intents=intents)

app = Flask("")

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.red())
        prefix = self.context.clean_prefix
        for cog, commands_list in mapping.items():
            commands_list = [c for c in commands_list if not c.hidden]
            if commands_list:
                command_text = '\n'.join([f'`{prefix}{c.name}`: {c.help}' for c in commands_list])
                embed.add_field(
                    name=cog.qualified_name if cog else "No Category", 
                    value=command_text, 
                    inline=False
                )
        
        await self.get_destination().send(embed=embed)

bot.help_command = HelpCommand()

@bot.event
async def on_ready():
    print('Synced slash commands for all guilds.')
    print(f'Logged in as {bot.user}')
    print('------------------------------')
    try:
        for guild in bot.guilds:
            await bot.tree.sync(guild=guild)
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def main():
    async with bot:
        base_dir = pathlib.Path(__file__).parent
        cogs_path = base_dir / "Cogs"

        for cog_file in cogs_path.glob('*.py'):
            if cog_file.name == "__init__.py":
                continue

            cog_name = f"Cogs.{cog_file.stem}"
            print(f"Loading {cog_name}")
            await bot.load_extension(cog_name)

        try:
            await bot.start(DISCORD_TOKEN)
        except KeyboardInterrupt:
            print("Shutting down...")
            await bot.close()

asyncio.run(main())
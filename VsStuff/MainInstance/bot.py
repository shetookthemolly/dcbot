import os
import threading
import pathlib
import asyncio
from flask import Flask
from discord.ext import commands
from dotenv import load_dotenv
import discord


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

threading.Thread(target=run_flask).start()

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
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
    print(f'Logged in as {bot.user}')
    print('------------------------------')

async def main():
    cogs_path = pathlib.Path('./VsStuff/MainInstance/Cogs')
    for cog_file in cogs_path.glob('*.py'):
        cog_name = f"VsStuff.MainInstance.Cogs.{cog_file.stem}"
        await bot.load_extension(cog_name)
    await bot.run(DISCORD_TOKEN)

asyncio.run(main())
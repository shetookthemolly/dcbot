import os
import threading
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------------------------------')

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
        prefix = self.context.clean_prefix
        for cog, commands in mapping.items():
            if commands:
                command_list = '\n'.join([f'`{prefix}{command.name}`: {command.help}' for command in commands])
                embed.add_field(name=cog.qualified_name if cog else "No Category", value=command_list, inline=False)
        
        await self.get_destination().send(embed=embed)

bot.help_command = HelpCommand()

bot.run(DISCORD_TOKEN)
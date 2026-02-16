import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

prefix = ','

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------------------------------')

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of available commands:", color=discord.Color.blue())
        for cog, commands in mapping.items():
            if commands:
                command_list = '\n'.join([f'`{prefix}{command.name}`: {command.help}' for command in commands])
                embed.add_field(name=cog.qualified_name if cog else "No Category", value=command_list, inline=False)
        
        await self.get_destination().send(embed=embed)

@bot.command(name='ping', help='Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(DISCORD_TOKEN)
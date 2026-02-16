import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

prefix = ','

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='ping', help='Responds with Pong')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @bot.command(name='echo', help='Echoes the provided message')
    async def echo(self, ctx, *, message):
        embed = discord.Embed(title=f'{self.bot.user} :p', description=f'{message}!', color=discord.Color.red())
        await ctx.send(embed=embed)

    @bot.command(name='av', help='Shows the avatar of the mentioned user or yourself if no user is mentioned')
    async def av(self, ctx, user: discord.User = None):
        embed = discord.Embed(title=f"{user.name}'s Avatar" if user else f"{ctx.author.name}'s Avatar", color=discord.Color.red())
        if user is None:
            user = ctx.author
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)
    

    @classmethod
    def setup(cls, bot):
        bot.add_cog(General(bot))
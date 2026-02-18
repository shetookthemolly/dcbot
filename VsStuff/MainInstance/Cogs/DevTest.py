import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True


class DevTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop', help='Stops the bot')
    @commands.is_owner()
    async def stop(self, ctx):
        embed = discord.Embed(title="Shutting down...", description="The bot is shutting down. Goodbye! (^///^)", color=discord.Color.red())
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.command(name='test', help='A simple test command')
    @commands.is_owner()
    async def test_command(self, ctx):
        await ctx.send("This is a test command.")

    @commands.command(name='sync', help='Syncs slash commands with Discord')
    @commands.is_owner()
    async def sync(self, ctx):
        await self.bot.tree.sync()
        embed = discord.Embed(title="Slash Commands Synced ⚙️", description="All slash commands have been synced with Discord.", color=discord.Color.red())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DevTest(bot))
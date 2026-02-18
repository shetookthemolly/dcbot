import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping', help='Responds with Pong')
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(name='echo', help='Echoes the provided message')
    async def echo(self, ctx, *, message):
        embed = discord.Embed(title=f'{self.bot.user.name} :p', description=f'{message}!', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='av', help='Shows the avatar of the mentioned user or yourself if no user is mentioned')
    async def av(self, ctx, user: discord.User = None):
        embed = discord.Embed(title=f"{user.name}'s Avatar" if user else f"{ctx.author.name}'s Avatar", color=discord.Color.red())
        if user is None:
            user = ctx.author
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)
    
    @app_commands.command(name="embed", description="Sends an embed with the provided title, content, and optional parameters")
    @app_commands.describe(
        title="The title of the embed (required)",
        content="The content of the embed (required)",
        color="The color of the embed (hex code, e.g., #FF5733) (optional)",
        footer="The footer text of the embed (optional)",
        thumbnail="URL of the thumbnail image (optional)",
        image="URL of the main image (optional)"
    )
    async def embed(
        self,
        interaction: discord.Interaction,
        title: str,
        content: str,
        color: str = None,  # Optional color
        footer: str = None,  # Optional footer text
        thumbnail: str = None,  # Optional thumbnail URL
        image: str = None  # Optional image URL
    ):
        await interaction.response.defer()

        try:    
            # Default color if not provided
            embed_color = int(color.lstrip("#"), 16) if color else discord.Color.red().value

            embed = discord.Embed(title=title, description=content, color=embed_color)

            # Add optional fields if provided
            if footer:
                embed.set_footer(text=footer)
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            if image:
                embed.set_image(url=image)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"An error occurred while creating the embed: {e}", ephemeral=True)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
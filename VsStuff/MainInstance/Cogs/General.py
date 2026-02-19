import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ping', help='Responds with Pong')
    async def ping(self, ctx):
        embed = discord.Embed(title=f'***From:*** {self.bot.user.name} :p', description=f'Pong!', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='echo', aliases=['ec', 'repeat'], help='Echoes the provided message')
    async def echo(self, ctx, *, message):
        embed = discord.Embed(title=f'***From:*** {self.bot.user.name} :p', description=f'{message}!', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['av', 'pfp'], help='Shows the avatar of the mentioned user or yourself if no user is mentioned')
    async def avatar(self, ctx, user: discord.User = None):
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
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            self.bot.sniped_messages[message.channel.id] = {
                "content": message.content,
                "author_name": message.author.name,
                "author_avatar": message.author.display_avatar.url,
                "author_id": message.author.id,
                "attachments": [a.url for a in message.attachments],
                "embeds": [e.to_dict() for e in message.embeds]
        }

    
    @commands.command(name='snipe', aliases=['s', 'sn'], help='Snipes the last deleted message in the channel')
    async def snipe(self, ctx):
        channel_id = ctx.channel.id

        if channel_id not in self.bot.sniped_messages:
            embed = discord.Embed(title="Error", description="There is no recently deleted message to snipe in this channel.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        sniped_message = self.bot.sniped_messages[channel_id]

        embed = discord.Embed(
            title=f"Sniped Message from {sniped_message['author_name']}",
            description=sniped_message['content'] or "No text content",
            color=discord.Color.red()
        )

        embed.set_author(
            name=sniped_message['author_name'],
            icon_url=sniped_message['author_avatar']
        )

        await ctx.send(embed=embed)

        for attachment in sniped_message['attachments']:
            await ctx.send(attachment)

        for embed_data in sniped_message['embeds']:
            await ctx.send(embed=discord.Embed.from_dict(embed_data))

        if sniped_message['author_id'] == self.bot.user.id:
            del self.bot.sniped_messages[channel_id]

    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
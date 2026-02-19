import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord import AllowedMentions

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.sniped_messages = {}

    @commands.command(name='ping', help='Responds with Pong')
    async def ping(self, ctx):
        embed = discord.Embed(title=f'Ping! :p', description=f'***From: *** {self.bot.user.mention} Pong! :p', color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='echo', aliases=['ec', 'repeat'], help='Echoes the provided message')
    async def echo(self, ctx, *, message):
        embed = discord.Embed(title=f'Echo! :p', description=f'***From:*** {self.bot.user.mention} {message}! :p', color=discord.Color.red())
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
            print(f"Message deleted in #{message.channel.name} by {message.author.name}: {message.content}")
            self.bot.sniped_messages[message.channel.id] = {
                "content": message.content,
                "author_name": message.author.name,
                "author_mention": message.author.mention,
                "author_avatar": message.author.display_avatar.url,
                "author_id": message.author.id,
                "attachments": [a.url for a in message.attachments],
                "embeds": [e.to_dict() for e in message.embeds]
        }

    
    @commands.command(name='snipe', aliases=['s', 'sn'], help='Snipes the last deleted message in the channel')
    async def snipe(self, ctx):
        channel_id = ctx.channel.id

        if channel_id not in self.bot.sniped_messages:
            embed = discord.Embed(title="Error ⚠️", description="There is no recently deleted message to snipe in this channel.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        sniped_message = self.bot.sniped_messages[channel_id]

        embed = discord.Embed(
            title=f"Sniped Message from `{ctx.channel.name}` chat 🔫",
            description=f"***from*** {sniped_message['author_mention']}***:*** {sniped_message['content'] or 'No text content'}",
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
    
    @commands.command(name='createrole', aliases=['cr'], help='Creates a new role with the specified name and color')
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, role_name, color: str = None):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            embed = discord.Embed(title="Error ⚠️", description=f"Role `{role_name}` already exists in this server.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        try:
            role_color = int(color.lstrip("#"), 16) if color else discord.Color.red().value
            new_role = await ctx.guild.create_role(name=role_name, color=role_color)
            embed = discord.Embed(title="Role Created ✅", description=f"Created a new role named `{new_role.name}` with color `{color or '#FF0000'}`.", color=discord.Color.red())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error ⚠️", description=f"An error occurred while creating the role: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @commands.command(name='deleterole', aliases=['dr'], help='Deletes the role with the specified name')
    @commands.has_permissions(manage_roles=True)
    async def deleterole(self, ctx, *, role_name):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            embed = discord.Embed(title="Error ⚠️", description=f"Role `{role_name}` not found in this server.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        try:
            await role.delete()
            embed = discord.Embed(title="Role Deleted ❌", description=f"Deleted the `{role_name}` role.", color=discord.Color.red())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="Error ⚠️", description=f"An error occurred while deleting the role: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='role', aliases=['r'], help='Adds a role to the user or removes it if they already have it')
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, user: discord.User, *, role_name):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            embed = discord.Embed(title="Error ⚠️", description=f"Role `{role_name}` not found in this server.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        if role in user.roles:
            await user.remove_roles(role)
            embed = discord.Embed(title="Role Removed ❌", description=f"Removed the `{role_name}` role from {user.mention} 👍", color=discord.Color.red())
        else:
            await user.add_roles(role)
            embed = discord.Embed(title="Role Added ✅", description=f"Added the `{role_name}` role to {user.mention} 👍", color=discord.Color.red())

        await ctx.send(embed=embed)

    @commands.command(name='roles', aliases=['rs'], help='Lists all roles in the server')
    async def roles(self, ctx):
        roles = [role for role in ctx.guild.roles if role.name != "@everyone"]
        if not roles:
            embed = discord.Embed(title="No Roles Found", description="There are no roles in this server.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        embed = discord.Embed(title="Server Roles:", description="\n".join([f"`{role.name}`" for role in roles]), color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='roleinfo', aliases=['ri'], help='Shows information about a specific role')
    async def roleinfo(self, ctx, *, role_name):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            embed = discord.Embed(title="Error ⚠️", description=f"Role `{role_name}` not found in this server.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        embed = discord.Embed(title=f"Role Information for: `{role.name}`", color=discord.Color.red())
        embed.add_field(name="ID", value=role.id, inline=False)
        embed.add_field(name="Color", value=str(role.color), inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='purge', aliases=['p', 'clear'], help='Deletes a specified number of messages from the channel')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(title="Error ⚠️", description="Please specify a positive number of messages to delete.", color=discord.Color.red())
            return await ctx.send(embed=embed)

        deleted = 0
        while amount > 0:
            batch_size = min(amount, 100)
            deleted_messages = await ctx.channel.purge(limit=batch_size)
            deleted += len(deleted_messages)
            amount -= batch_size

            await asyncio.sleep(1)

        embed = discord.Embed(title="Purge Complete ✅", description=f"Deleted {deleted} messages from this channel.", color=discord.Color.red())
        await ctx.send(embed=embed) 

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
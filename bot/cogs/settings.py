import discord
from discord.ext import commands
import data


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', description='Pong!', hidden=True)
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping', description=f'{int(self.bot.latency*100)} ms')
        await ctx.send(embed=embed)

    @commands.command(name='help', description='List all commands. Use help <command> for specific command.', usage='help <command>')
    async def help(self, ctx, *args):
        embed = discord.Embed(title='Help')
        embed.color = discord.Colour.blue()
        if len(args) == 0:
            for command in self.bot.commands:
                if command.hidden is False:
                    embed.add_field(
                        name=command.name,
                        value=command.description,
                        inline=False
                    )
        else:
            for command in self.bot.commands:
                if command.name == args[0] and command.hidden is False:
                    embed.add_field(
                        name=f'`{command.name}`',
                        value=command.description,
                        inline=False
                    )
                    embed.add_field(
                        name='Usage',
                        value=command.usage,
                        inline=False
                    )
                    break
        await ctx.send(embed=embed)

    @commands.command(name='roomcat', description='Set the room category', usage='roomcat <category_id>')
    async def roomcat(self, ctx, *args):
        embed = discord.Embed(title='Room Category')
        if len(args) > 1 or len(args) == 0:
            embed.add_field(
                name='Error',
                value=f'Please enter a valid category ID'
            )
            embed.colour = discord.Colour.red()
        else:
            category = args[0]
            cat = discord.utils.get(ctx.guild.categories, id=int(category))
            if not cat:
                embed.add_field(
                    name='Error',
                    value=f'Category `{category}` not found'
                )
                embed.colour = discord.Colour.red()
            elif category == 'none' or category == 'default':
                embed = discord.Embed(
                    title='Removed Room Category',
                    description=f'**`{cat.name}`**'
                )
                embed.colour = discord.Colour.blue()
                data.guild.roomcat = None
            elif cat == data.guild.roomcat:
                embed.add_field(
                    name='Error',
                    value=f'Category `{category}` is already Room Category'
                )
                embed.colour = discord.Colour.red()
            else:
                data.guild.roomcat = cat.id
                embed.add_field(name='Changed Room Category',
                                value=f'`{cat.name}`')
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

    @commands.command(name='roomname', description='Set the name of the room', usage='roomname <name>')
    async def roomname(self, ctx, *args):
        embed = discord.Embed(title='Room Name')
        if len(args) == 0:
            embed.add_field(
                name='Error',
                value='Enter a valid room name'
            )
            embed.colour = discord.Colour.red()
        else:
            roomname = ' '.join(args)
            if roomname == 'default':
                data.guild.roomname = 'Room'
            else:
                data.guild.roomname = roomname
            embed.add_field(
                name='Changed Room Name',
                value=f'Room name changed to `{data.guild.roomname}`'
            )
            embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

    @commands.command(name='lock', description='Lock the room', usage='lock (while room is joined)')
    async def lockroom(self, ctx):
        embed = discord.Embed(title='Lock Room')
        if not ctx.author.voice or str(ctx.author.voice.channel.id) not in data.guild.newchannels.keys():
            embed.add_field(
                name='Error',
                value='You are not connected to any custom voice channel'
            )
        elif str(ctx.author.voice.channel.id) in data.guild.newchannels.keys():
            if data.guild.newchannels[str(ctx.author.voice.channel.id)]:
                embed.add_field(
                    name='Room Locked',
                    value=f'Your room {ctx.author.voice.channel} is already locked'
                )
            else:
                embed.add_field(
                    name='Room Locked',
                    value=f'Your room {ctx.author.voice.channel} has been locked'
                )
                data.guild.newchannels[str(ctx.author.voice.channel.id)] = True
        await ctx.send(embed=embed)

    @commands.command(name='unlock', description='Unlock the room', usage='unlock (while room is joined)')
    async def unlockroom(self, ctx):
        embed = discord.Embed(title='Unlock Room')
        if not ctx.author.voice or ctx.author.voice.channel.id not in data.guild.newchannels.keys():
            embed.add_field(
                name='Error',
                value='You are not connected to any custom voice channel'
            )
        else:
            if data.guild.newchannels[str(ctx.author.voice.channel.id)]:
                embed.add_field(
                    name='Room Unocked',
                    value=f'Your room {ctx.author.voice.channel} has been unlocked'
                )
                data.guild.newchannels[
                    str(ctx.author.voice.channel.id)] = False
            else:
                embed.add_field(
                    name='Error',
                    value=f'Your room {ctx.author.voice.channel} is already unlocked'
                )
        await ctx.send(embed=embed)

    @commands.command(name='config', description='Show bot configuration for the server', usage='config')
    async def config(self, ctx):
        embed = discord.Embed(title='Configuration')
        channels = data.guild.channels
        if not channels:
            embed.add_field(
                name=None,
                value='No channels in configuration'
            )
            embed.colour = discord.Colour.red()
        else:
            embed.add_field(
                name='Channels',
                value='\n'.join(
                    [f'`{x.name}` - `{x.category}`' for x in [
                        discord.utils.get(
                            ctx.guild.voice_channels,
                            id=int(y)
                        ) for y in channels]]
                ),
                inline=False
            )
        if data.guild.roomcat:
            embed.add_field(
                name='Room Category',
                value=f'`{discord.utils.get(ctx.guild.categories, id = data.guild.roomcat).name}`'
            )
        embed.add_field(
            name='Rooom Name',
            value=f'`{data.guild.roomname}`'
        )
        embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

    @commands.command(name='prefix', description='Set the prefix for the server', usage='prefix <prefix>')
    async def setprefix(self, ctx, *args):
        embed = discord.Embed(title='Change Prefix')
        if len(args) > 1 or len(args) == 0:
            embed.add_field(
                name='Error',
                value=f'Please enter a valid prefix'
            )
            embed.colour = discord.Colour.red()
        else:
            prefix = str(args[0])
            if prefix == data.guild.prefix:
                embed.add_field(
                    name='Error',
                    value=f'{prefix} is already set prefix'
                )
                embed.colour = discord.Colour.red()
            else:
                if prefix == 'default':
                    prefix = '+cr'
                    data.guild.prefix = prefix
                else:
                    data.guild.prefix = prefix
                embed.add_field(
                    name='Changed Prefix',
                    value=f'{prefix} has been set as bot prefix'
                )
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

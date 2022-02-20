import discord
from discord.ext import commands
import data


class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Ping', description=f'{int(self.bot.latency*100)} ms')
        await ctx.send(embed=embed)

    @commands.command(name='roomcat')
    async def roomcat(self, ctx, *args):
        embed = discord.Embed(title='Room Category')
        if len(args) > 1 or len(args) == 0:
            embed.add_field(
                name='Error', value=f'Please enter a valid category ID')
            embed.colour = discord.Colour.red()
        else:
            category = int(args[0])
            cat = discord.utils.get(ctx.guild.categories, id=category)
            if not cat:
                embed.add_field(
                    name='Error', value=f'Category `{category}` not found')
                embed.colour = discord.Colour.red()
            elif category == 'none' or category == 'default':
                embed = discord.Embed(
                    title='Removed Room Category', description=f'**`{cat.name}`**')
                embed.colour = discord.Colour.blue()
                data.guild.roomcat = None
            elif cat == data.guild.roomcat:
                embed.add_field(
                    name='Error', value=f'Category `{category}` is already Room Category')
                embed.colour = discord.Colour.red()
            else:
                data.guild.roomcat = cat.id
                embed.add_field(name='Changed Room Category',
                                value=f'`{cat.name}`')
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

    @commands.command(name='roomname')
    async def roomname(self, ctx, *args):
        embed = discord.Embed(title='Room Name')
        if len(args) == 0:
            embed.add_field(name='Error', value='Enter a valid room name')
            embed.colour = discord.Colour.red()
        else:
            roomname = ' '.join(args)
            if roomname == 'default':
                data.guild.roomname = '%USERNAME%\'s Room'
            else:
                data.guild.roomname = roomname
            embed.add_field(name='Changed Room Name',
                            value=f'Room name changed to `{data.guild.roomname}`')
            embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

    @commands.command(name='lock')
    async def lockroom(self, ctx):
        embed = discord.Embed(title='Lock Room')
        if not ctx.author.voice or str(ctx.author.voice.channel.id) not in data.guild.newchannels.keys():
            embed.add_field(
                name='Error', value='You are not connected to any custom voice channel')
        elif str(ctx.author.voice.channel.id) in data.guild.newchannels.keys():
            if data.guild.newchannels[str(ctx.author.voice.channel.id)]:
                embed.add_field(
                    name='Room Locked', value=f'Your room {ctx.author.voice.channel} is already locked')
            else:
                embed.add_field(
                    name='Room Locked', value=f'Your room {ctx.author.voice.channel} has been locked')
                data.guild.newchannels[str(ctx.author.voice.channel.id)] = True
        await ctx.send(embed=embed)

    @commands.command(name='unlock')
    async def unlockroom(self, ctx):
        embed = discord.Embed(title='Unlock Room')
        if not ctx.author.voice or ctx.author.voice.channel.id not in data.guild.newchannels.keys():
            embed.add_field(
                name='Error', value='You are not connected to any custom voice channel')
        else:
            if data.guild.newchannels[str(ctx.author.voice.channel.id)]:
                embed.add_field(
                    name='Room Unocked', value=f'Your room {ctx.author.voice.channel} has been unlocked')
                data.guild.newchannels[
                    str(ctx.author.voice.channel.id)] = False
            else:
                embed.add_field(
                    name='Error', value=f'Your room {ctx.author.voice.channel} is already unlocked')
        await ctx.send(embed=embed)

    @commands.command(name='config')
    async def config(self, ctx):
        embed = discord.Embed(title='Configuration')
        channels = data.guild.channels
        if not channels:
            embed.add_field(name=None, value='No channels in configuration')
            embed.colour = discord.Colour.red()
        else:
            embed.add_field(name='Channels', value='\n'.join([f'`{x.name}` - `{x.category}`' for x in [
                            discord.utils.get(ctx.guild.voice_channels, id=int(y)) for y in channels]]), inline=False)
        if data.guild.roomcategory:
            embed.add_field(
                name='Room Category', value=f'`{discord.utils.get(ctx.guild.categories,id = data.guild.roomcategory).name}`')
        embed.add_field(name='Rooom Name',
                        value=f'`{data.guild.roomname}`')
        embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

    @commands.command(name='setprefix')
    async def setprefix(self, ctx, *args):
        embed = discord.Embed(title='Change Prefix')
        if len(args) > 1 or len(args) == 0:
            embed.add_field(name='Error', value=f'Please enter a valid prefix')
            embed.colour = discord.Colour.red()
        else:
            prefix = str(args[0])
            if prefix == data.guild.prefix:
                embed.add_field(
                    name='Error', value=f'{prefix} is already set prefix')
                embed.colour = discord.Colour.red()
            else:
                if prefix == 'default':
                    prefix = '+cr'
                    data.guild.prefix = prefix
                else:
                    data.guild.prefix = prefix
                embed.add_field(name='Changed Prefix',
                                value=f'{prefix} has been set as bot prefix')
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

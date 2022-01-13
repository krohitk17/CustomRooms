import discord
from discord.ext import commands
import channellist as cl
import customrooms as cr


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
                cl.guilds .roomcat = None
            elif cat == cl.guilds .roomcat:
                embed.add_field(
                    name='Error', value=f'Category `{category}` is already Room Category')
                embed.colour = discord.Colour.red()
            else:
                cl.guilds .roomcat = cat.id
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
                cl.guilds .roomname = '%USERNAME%\'s Room'
            else:
                cl.guilds .roomname = roomname
            embed.add_field(name='Changed Room Name',
                            value=f'Room name changed to `{cl.guilds .roomname}`')
            embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

    @commands.command(name='lock')
    async def lockroom(self, ctx):
        embed = discord.Embed(title='Lock Room')
        if not ctx.author.voice or ctx.author.voice.channel.id not in cl.guilds .new_channels.keys():
            embed.add_field(
                name='Error', value='You are not connected to any custom voice channel')
        if ctx.author.voice.channel.id in cl.guilds .new_channels.keys():
            if cl.guilds .new_channels[ctx.author.voice.channel.id]:
                embed.add_field(
                    name='Room Unocked', value=f'Your room {ctx.author.voice.channel} is already locked')
            else:
                embed.add_field(
                    name='Room Locked', value=f'Your room {ctx.author.voice.channel} has been locked')
            cl.guilds .roomname[ctx.author.voice.channel.id] = True
        await ctx.send(embed=embed)

    @commands.command(name='unlock')
    async def unlockroom(self, ctx):
        embed = discord.Embed(title='Unlock Room')
        if not ctx.author.voice or ctx.author.voice.channel.id not in cl.guilds .new_channels.keys():
            embed.add_field(
                name='Error', value='You are not connected to any custom voice channel')
        else:
            if cl.guilds .roomname[int(ctx.author.voice.channel.id)]:
                embed.add_field(
                    name='Room Unocked', value=f'Your room {ctx.author.voice.channel} has been unlocked')
                cl.guilds .roomaname[
                    int(ctx.author.voice.channel.id)] = False
            else:
                embed.add_field(
                    name='Error', value=f'Your room {ctx.author.voice.channel} is already unlocked')
        await ctx.send(embed=embed)

    @commands.command(name='config')
    async def config(self, ctx):
        embed = discord.Embed(title='Configuration')
        channels = cl.guilds .channels
        categories = cl.guilds .bindcategory
        if not channels:
            embed.add_field(name=None, value='No channels in configuration')
            embed.colour = discord.Colour.red()
        else:
            embed.add_field(name='Channels', value='\n'.join([f'`{x.name}` - `{x.category}`' for x in [
                            discord.utils.get(ctx.guild.voice_channels, id=int(y)) for y in channels]]), inline=False)
        if categories:
            embed.add_field(name='Binded Categories', value='\n'.join([f'`{x.name}`' for x in [
                            discord.utils.get(ctx.guild.categories, id=int(y)) for y in categories]]))
        if cl.guilds .roomcategory:
            embed.add_field(
                name='Room Category', value=f'`{discord.utils.get(ctx.guild.categories,id = cl.guilds .roomcategory).name}`')
        embed.add_field(name='Rooom Name',
                        value=f'`{cl.guilds .roomname}`')
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
            if prefix == cl.guilds .prefix:
                embed.add_field(
                    name='Error', value=f'{prefix} is already set prefix')
                embed.colour = discord.Colour.red()
            else:
                if prefix == 'default':
                    prefix = cr.PREFIX
                    cl.guilds .prefix = prefix
                else:
                    cl.guilds .prefix = prefix
                embed.add_field(name='Changed Prefix',
                                value=f'{prefix} has been set as bot prefix')
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)

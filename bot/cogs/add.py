import discord
from discord.ext import commands
import data


class Add(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    async def addchannel(self, ctx, *args):
        embed = discord.Embed(title='Add Channel')
        if len(args) > 1 or len(args) == 0 or not ''.join(args).isnumeric():
            embed.add_field(
                name='Error', value=f'Please enter a valid channel ID')
            embed.colour = discord.Colour.red()
        else:
            channel = int(args[0])
            ch = discord.utils.get(ctx.guild.voice_channels, id=channel)
            if not ch:
                embed.add_field(
                    name='Error', value=f'Channel `{channel}` not found')
                embed.colour = discord.Colour.red()
            elif ch.id in data.guild.channels:
                embed.add_field(
                    name='Error', value=f'Channel `{ch.name}` already in configuration')
                embed.colour = discord.Colour.red()
            else:
                embed.add_field(
                    name='Added Channel', value=f'**Channel Name : `{ch.name}`\nCategory : `{ch.category}`**')
                data.guild.channels.append(ch.id)
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

    @commands.command(name='addcat')
    async def addcat(self, ctx, *args):
        embed = discord.Embed(title='Add Category')
        if len(args) > 1 or len(args) == 0 or not ''.join(args).isnumeric():
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
            else:
                for i in ctx.guild.voice_channels:
                    if i.category == cat:
                        data.guild.channels.append(int(i.id))
                embed.add_field(
                    name='Added Category', value=f'All voice channels inside `{cat.name}` added to configuration')
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

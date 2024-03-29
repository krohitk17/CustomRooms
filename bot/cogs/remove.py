import discord
from discord.ext import commands
import asyncio
import data


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rm', description='Remove a channel from configuration', usage='rm <channel_id>')
    async def rmchannel(self, ctx, *args):
        embed = discord.Embed(title='Remove Channel')
        if len(args) > 1 or len(args) == 0 or not ''.join(args).isnumeric():
            embed.add_field(
                name='Error',
                value=f'Please enter a valid channel ID'
            )
            embed.colour = discord.Colour.red()
        else:
            channel = int(args[0])
            ch = discord.utils.get(ctx.guild.voice_channels, id=channel)
            if not ch:
                embed.add_field(
                    name='Error',
                    value=f'Channel `{channel}` not found'
                )
                embed.colour = discord.Colour.red()
            elif ch.id in data.guild.channels:
                data.guild.channels.remove(int(ch.id))
                embed.add_field(
                    name='Channel',
                    value=f'`{ch.name}` removed from Configuration'
                )
                embed.colour = discord.Colour.blue()
            else:
                embed.add_field(
                    name='Error',
                    value=f'Channel `{ch.name}` not in Cofiguration'
                )
                embed.colour = discord.Colour.red()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

    @commands.command(name='rmcat', description='Remove a category from configuration', usage='rmcat <category_id>')
    async def rmcat(self, ctx, *args):
        embed = discord.Embed(title='Remove Category')
        if len(args) > 1 or len(args) == 0 or not ''.join(args).isnumeric():
            embed.add_field(
                name='Error',
                value=f'Please enter a valid category ID'
            )
            embed.colour = discord.Colour.red()
        else:
            category = int(args[0])
            cat = discord.utils.get(ctx.guild.categories, id=category)
            if not cat:
                embed.add_field(
                    name='Error',
                    value=f'Category `{category}` not found'
                )
                embed.colour = discord.Colour.red()
            else:
                for i in ctx.guild.voice_channels:
                    if i.category == cat:
                        data.guild.channels.remove(int(i.id))
                embed.add_field(
                    name='Removed Category',
                    value=f'All voice channels inside `{cat.name}` removed from configuration'
                )
                embed.colour = discord.Colour.blue()
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

    @commands.command(name='rmconfig', description='Remove a category from configuration', usage='rmconfig')
    async def rmconfig(self, ctx):
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ["🇾", "🇳"]
        embed = discord.Embed(title='Remove Configuration')
        embed.add_field(
            name='Are You Sure?',
            value='This will remove all configuration for the server.'
        )
        embed.colour = discord.Colour.dark_gold()
        message = await ctx.send(embed=embed)
        for i in ["🇾", "🇳"]:
            await message.add_reaction(i)
        try:
            reaction = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='Remove Configuration',
                description='Timed Out'
            )
            embed.colour = discord.Colour.red()
            await ctx.send(embed=embed)
        else:
            if reaction[0].emoji == "🇾":
                data.removeserver(ctx.guild.id)
                data.newserver(ctx.guild.id)
                data.guild = data.getserver(ctx.guild.id)
                embed = discord.Embed(
                    title='Remove Configuration',
                    description='Configuration Removed'
                )
                embed.colour = discord.Colour.blue()
                await ctx.send(embed=embed)
            elif reaction[0].emoji == "🇳":
                embed = discord.Embed(
                    title='Remove Configuration',
                    description='Cancelled'
                )
                embed.colour = discord.Colour.red()
                await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command('config'))

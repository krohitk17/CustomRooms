from discord.ext import commands
import channellist as cl
import asyncio


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cl.new_server(guild)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        cl.update_server(ctx.guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            if after.channel.id in cl.guilds.channels:
                cat = cl.guilds.roomcategory
                if not cat:
                    cat = after.channel.category
                roomname = cl.guilds.roomname.replace(
                    '%USERNAME%', f'{member.name}')
                ch = await member.guild.create_voice_channel(name=roomname, category=cat)
                cl.guilds.new_channels[ch.id] = False
                await member.move_to(ch)
            if after.channel.id in cl.guilds.new_channels.keys():
                if cl.guilds.new_channels[after.channel.id]:
                    await member.move_to(None)
        if before.channel:
            if before.channel.id in cl.guilds.new_channels.keys() and not before.channel.members:
                await before.channel.delete()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.id in cl.guilds.channels:
            cl.guilds.channels.remove(channel.id)
        if channel.id in cl.guilds.new_channels.keys():
            cl.guilds.new_channels.pop(channel.id)
        if channel.id == cl.guilds.roomcategory:
            cl.guilds.roomcategory = None
        if channel.id in cl.guilds.bindcategory:
            cl.guilds.bindcategory.remove(channel.id)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await asyncio.sleep(2)
        if channel.category.id in cl.guilds.bindcategory:
            if channel.id not in cl.guilds.new_channels.keys():
                cl.guilds.channels.append(channel.id)

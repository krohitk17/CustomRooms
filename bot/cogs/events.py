from discord.ext import commands
import data
import database as db
import models


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        session = db.localsession()
        guilds = session.query(models.guild).all()
        for guild in self.bot.guilds:
            if guild.id not in guilds:
                data.newserver(guild.id)
        session.close()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data.newserver(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        data.removeserver(guild.id)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        data.updateserver(data.guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = data.getserver(member.guild.id)
        if after.channel:
            if after.channel.id in guild.channels:
                cat = guild.roomcategory
                if not cat:
                    cat = after.channel.category
                roomname = guild.roomname.replace(
                    '%USERNAME%', f'{member.name}')
                ch = await member.guild.create_voice_channel(name=roomname, category=cat)
                guild.newchannels[str(ch.id)] = False
                await member.move_to(ch)
            if str(after.channel.id) in guild.newchannels.keys():
                print('someone joined')
                if guild.newchannels[str(after.channel.id)]:
                    print('someone kicked')
                    await member.move_to(None)
        if before.channel:
            if str(before.channel.id) in guild.newchannels.keys() and not before.channel.members:
                await before.channel.delete()
                guild.newchannels.pop(str(before.channel.id))
        data.updateserver(guild)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = data.getserver(channel.guild.id)
        if channel.id in guild.channels:
            guild.channels.remove(channel.id)
        if channel.id == guild.roomcategory:
            guild.roomcategory = None
        data.updateserver(guild)

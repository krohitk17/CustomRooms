import asyncio
from discord.ext import commands
import customrooms as cr
import channellist as cl
from cogs import add
from cogs import remove
from cogs import settings

bot = commands.Bot(command_prefix=cl.getPrefix, case_insensitive='True')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_guild_join(guild):
    cl.new_server(guild)


@bot.event
async def on_command_completion(ctx):
    cl.update_server(ctx.guild)


@bot.event
async def on_voice_state_update(member, before, after):
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


@bot.event
async def on_guild_channel_delete(channel):
    if channel.id in cl.guilds.channels:
        cl.guilds.channels.remove(channel.id)
    if channel.id in cl.guilds.new_channels.keys():
        cl.guilds.new_channels.pop(channel.id)
    if channel.id == cl.guilds.roomcategory:
        cl.guilds.roomcategory = None
    if channel.id in cl.guilds.bindcategory:
        cl.guilds.bindcategory.remove(channel.id)


@bot.event
async def on_guild_channel_create(channel):
    await asyncio.sleep(2)
    if channel.category.id in cl.guilds.bindcategory:
        if channel.id not in cl.guilds.new_channels.keys():
            cl.guilds.channels.append(channel.id)

bot.add_cog(add.Add(bot))
bot.add_cog(remove.Remove(bot))
bot.add_cog(settings.Settings(bot))

if __name__ == '__main__':
    try:
        bot.run(cr.TOKEN)
    except:
        print('Invalid Token')

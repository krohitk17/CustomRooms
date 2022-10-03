import discord
from discord.ext import commands

import os
import models
import data
import database as db

from cogs import events
from cogs import settings
from cogs import remove
from cogs import add


def getPrefix(bot, message):
    data.guild = data.getserver(message.guild.id)
    return data.guild.prefix


def getToken():
    try:
        return os.environ['TOKEN']
    except:
        print('Token Not Found!')
        exit()


bot = commands.Bot(
    command_prefix=getPrefix,
    case_insensitive='True',
    help_command=None
)


if __name__ == '__main__':
    models.base.metadata.create_all(bind=db.engine)
    bot.add_cog(events.Events(bot))
    bot.add_cog(add.Add(bot))
    bot.add_cog(remove.Remove(bot))
    bot.add_cog(settings.Settings(bot))
    bot.activity = discord.Activity(
        type=discord.ActivityType.watching,
        name='you'
    )
    bot.run(getToken())

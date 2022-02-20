from cogs import events
from cogs import settings
from cogs import remove
from cogs import add
from discord.ext import commands
import os
import models
import data
import database as db


def getPrefix(bot, message):
    data.guild = data.getserver(message.guild.id)
    return data.guild.prefix


def getToken():
    return os.environ['TOKEN']


bot = commands.Bot(command_prefix=getPrefix, case_insensitive='True')


if __name__ == '__main__':
    models.base.metadata.create_all(bind=db.engine)
    bot.add_cog(events.Events(bot))
    bot.add_cog(add.Add(bot))
    bot.add_cog(remove.Remove(bot))
    bot.add_cog(settings.Settings(bot))
    bot.run(getToken())

from discord.ext import commands
import customrooms as cr
import channellist as cl
from cogs import add
from cogs import remove
from cogs import settings
from cogs import events

bot = commands.Bot(command_prefix=cl.getPrefix, case_insensitive='True')

if __name__ == '__main__':
    try:
        bot.add_cog(events.Events(bot))
        bot.add_cog(add.Add(bot))
        bot.add_cog(remove.Remove(bot))
        bot.add_cog(settings.Settings(bot))
        bot.run(cr.TOKEN)
    except:
        print('Invalid Token')

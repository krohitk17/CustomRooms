import data
import models
import database as db

guild = models.guild(
    id=1,
    prefix='+cr',
    channels=[],
    new_channels={},
    roomcategory=None,
    roomname='%USERNAME%\'s Room'
)
models.base.metadata.create_all(bind=db.engine)
data.newserver(guild.id)
print(data.getserver(guild.id).id)
guild.prefix = '-cr'
data.updateserver(guild)
print(data.getserver(guild.id).prefix)
data.removeserver(guild.id)

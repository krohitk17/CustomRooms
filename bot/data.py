import database as db
import models

global guild
guild = None


def newserver(server):
    session = db.localsession()
    guild = models.guild(
        id=server,
        prefix='+cr',
        channels=[],
        new_channels={},
        roomcategory=None,
        roomname='%USERNAME%\'s Room'
    )
    session.add(guild)
    session.commit()
    session.close()
    return guild


def updateserver(server):
    session = db.localsession()
    guild = session.query(models.guild).filter_by(id=server.id).first()
    guild.prefix = server.prefix
    guild.channels = server.channels
    guild.newchannels = server.newchannels
    guild.roomcategory = server.roomcategory
    guild.roomname = server.roomname
    session.commit()
    session.close()


def removeserver(server):
    session = db.localsession()
    guild = session.query(models.guild).filter_by(id=server).first()
    session.delete(guild)
    session.commit()
    session.close()


def getserver(server):
    session = db.localsession()
    guild = session.query(models.guild).filter_by(id=server).first()
    session.close()
    return guild

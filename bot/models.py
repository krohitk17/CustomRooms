from sqlalchemy import *
from sqlalchemy.ext.mutable import MutableList, MutableDict
from database import base


class guild(base):
    __tablename__ = 'guilds'
    id = Column(Integer, primary_key=True)
    prefix = Column(String(5), nullable=False)
    channels = MutableList.as_mutable(Column(JSON, nullable=False, default=[]))
    newchannels = MutableDict.as_mutable(
        Column(JSON, nullable=False, default={})
    )
    roomcat = Column(Integer, nullable=True)
    roomname = Column(String(50), nullable=False, default='%USERNAME%\'s Room')

    def __init__(self, id, prefix, channels, new_channels, roomcat, roomname):
        self.id = id
        self.prefix = prefix
        self.channels = channels
        self.new_channels = new_channels
        self.roomcat = roomcat
        self.roomname = roomname

    def __repr__(self):
        return str(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'prefix': self.prefix,
            'channels': self.channels,
            'newchannels': self.newchannels,
            'roomcat': self.roomcat,
            'roomname': self.roomname
        }

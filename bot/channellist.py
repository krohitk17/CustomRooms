import customrooms as cr
import json
import sys


class guild_list():
    def __init__(self):
        self.prefix = cr.PREFIX
        self.channels = list()
        self.new_channels = dict()
        self.roomcategory = str()
        self.roomname = '%USERNAME%\'s Room'
        self.bindcategory = list()


global guilds, path
guilds = guild_list()
path = sys.path[0]+'/data'


def new_server(guild):
    print(guild.id)
    with open(f'{path}/{guild.id}.txt', 'x') as file:
        guilds.id = guild.id
        json.dump(guilds.__dict__, file, indent=2)
        print(f'New Server : {guild.name}')


def update_server(guild):
    with open(f'{path}/{guild.id}.txt', 'w') as file:
        json.dump(guilds.__dict__, file, indent=2)


def load_server(guild):
    try:
        print('Opening file')
        file = open(f'{path}/{guild.id}.txt', 'x')
    except:
        print('File doesn\'t exist')
        update_server(guild)
        print('Created file')
    finally:
        with open(f'{path}/{guild.id}.txt', 'r') as file:
            guild = json.load(file)
            guilds.prefix = guild['prefix']
            guilds.channels = guild['channels']
            guilds.new_channels = guild['new_channels']
            guilds.roomcategory = guild['roomcategory']
            guilds.roomname = guild['roomname']
            guilds.bindcategory = guild['bindcategory']


def getPrefix(bot, message):
    load_server(message.guild)
    return guilds.prefix

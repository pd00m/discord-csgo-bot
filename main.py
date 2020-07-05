import json
import time
import math
from threading import Timer

import discord
from discord.ext import commands
import a2s

class server_info():
    def __init__(self, config):
        self.config = config
        self.ip_address = config.get('server_ip')
        self.server_port = config.get('server_port')
        self.connect_link = 'steam://connect/' + str(self.ip_address) + ':' + str(self.server_port) + '/'
        print('Loaded server config: ' + self.ip_address + ':' + str(self.server_port))

    def get(self):
        print("getting server info...")
        try:
            server_info = a2s.info((self.ip_address, self.server_port ))
            self.server_name = server_info.server_name
            self.curr_map = server_info.map_name
            self.players = str(server_info.player_count) + '/' + str(server_info.max_players)
            self.ping = str(int((server_info.ping* 1000))) + 'ms'
            print('Server: ' + self.ip_address + ':' + str(self.server_port) + ' | Ping: ' + self.ping + ' | Map: ' + self.curr_map + ' | Players: ' + self.players)

        except:
            print('Server down :(')
            self.server_name = 'Server down :('
            self.curr_map = 'Unknown'
            self.players = 0
            self.ping = '999ms'

# Refresh server info every n seconds     
def refresh_server_info():
    server_info.get()
    Timer(config.get('refresh_time'), refresh_server_info).start()   

# Load the config file
with open("config.json") as json_file:
    config = json.load(json_file)

client = commands.Bot(command_prefix=config.get('command_prefix'))

server_info = server_info(config) 
refresh_server_info()

@client.event
async def on_ready():
    status = server_info.curr_map + ' | ' + server_info.players
    await client.change_presence(activity=discord.Game(name=status))
    print('Bot logged in as {0.user}'.format(client))

@client.command()
async def server(ctx):   
    server_info.get()
    status = server_info.curr_map + ' | ' + server_info.players  
    embedVar = discord.Embed(title=server_info.server_name, description=server_info.connect_link, color=0x00ff00)
    embedVar.add_field(name='Ping', value=server_info.ping, inline=False)
    embedVar.add_field(name='Players', value=server_info.players, inline=False)
    embedVar.add_field(name='Map', value=server_info.curr_map, inline=False)  
    await client.change_presence(activity=discord.Game(name=status))    
    await ctx.send(embed=embedVar)

client.run(config.get('token'))




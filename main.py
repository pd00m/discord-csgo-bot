import json
import asyncio

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
            self.player_list = a2s.players((self.ip_address, self.server_port))
            self.server_name = server_info.server_name
            self.curr_map = server_info.map_name
            self.players = str(server_info.player_count) + '/' + str(server_info.max_players)
            self.ping = str(int((server_info.ping* 1000))) + 'ms'
            print('Server: ' + self.ip_address + ':' + str(self.server_port) + ' | Ping: ' + self.ping + ' | Map: ' + self.curr_map + ' | Players: ' + self.players)

        except:
            print('Server down :(')
            self.server_name = 'Server down :('
            self.curr_map = 'Unknown'
            self.players = '0'
            self.playerstats = 'Unknown'
            self.ping = '999ms'

# Refresh server info every n seconds     
async def refresh_server_info():
    while(True):
        server_info.get()
        status = server_info.curr_map + ' | ' + server_info.players
        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(config.get('refresh_time'))

# Load the config file
with open("config.json") as json_file:
    config = json.load(json_file)

client = commands.Bot(command_prefix=config.get('command_prefix'))

server_info = server_info(config)

@client.event
async def on_ready():
    client.loop.create_task(refresh_server_info())
    print('Bot logged in as {0.user}'.format(client))

# !server
@client.command()
async def server(ctx):   
    server_info.get()
    status = server_info.curr_map + ' | ' + server_info.players  
    embedVar = discord.Embed(title=server_info.server_name, color=0x00ff00) 
    if(len(config.get('custom_thumb')) > 0):
        embedVar.set_thumbnail(url=config.get('custom_thumb'))
    if(len(config.get('custom_banner')) > 0):
        embedVar.set_image(url=config.get('custom_banner'))
    embedVar.add_field(name='Connect', value=server_info.connect_link, inline=False)
    embedVar.add_field(name='Map', value=server_info.curr_map, inline=True)
    embedVar.add_field(name='Players', value=server_info.players, inline=True)
    embedVar.add_field(name='Ping', value=server_info.ping, inline=True)
    embedVar.add_field(name='\u200b', value='\u200b', inline=False)
    for player in server_info.player_list:
            playerscore =  str(player.score) + ' Kills'
            embedVar.add_field(name=player.name, value=playerscore, inline=True)    
    await client.change_presence(activity=discord.Game(name=status))    
    await ctx.send(embed=embedVar)

# !ip
@client.command()
async def ip(ctx):   
    await ctx.send(server_info.connect_link)

# !about
@client.command()
async def about(ctx):
    embedVar = discord.Embed(title='discord-csgo-bot', color=0x00ff00)
    embedVar.add_field(name='gitHub', value='https://github.com/pd00m/discord-csgo-bot', inline=False)
    await ctx.send(embed=embedVar)

client.run(config.get('token'))




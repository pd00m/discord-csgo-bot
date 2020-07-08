import json
import asyncio
from datetime import datetime, timedelta

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

        try:
            server_info = a2s.info((self.ip_address, self.server_port ))
            self.player_list = a2s.players((self.ip_address, self.server_port))
            self.server_name = server_info.server_name
            self.curr_map = server_info.map_name.split('/')[-1]
            self.players = str(server_info.player_count) + '/' + str(server_info.max_players)
            self.ping = str(int((server_info.ping* 1000))) + 'ms'

        except:
            print('Server down :(')
            self.server_name = 'Server down :('
            self.curr_map = 'Unknown'
            self.players = '0'
            self.playerstats = 'Unknown'
            self.ping = '999ms'

class mm_player():
    def __init__(self, author):
        self.author = author
        self.init_time = datetime.now()
        self.time_diff = timedelta(seconds=0)


# Refresh server info every n seconds     
async def refresh_server_info():
    while(True):
        server_info.get()
        status = server_info.curr_map + ' | ' + server_info.players
        await client.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(config.get('refresh_time'))

# check for inactive matchmaking search status every n minutes, after this, remove player from list
async def check_mm_state():
    while(True):
        for player in mm_player_list:
            player.time_diff = datetime.now() - player.init_time
            if int((player.time_diff.total_seconds() / 60) % 60) > config.get('mm_status_reset_minutes', 30):
                mm_player_list.remove(player)
        await asyncio.sleep(60)


def player_exists(iterable):
    for element in iterable:
        if element:
            return True
    return False

# Load the config file
with open("config.json") as json_file:
    config = json.load(json_file)

client = commands.Bot(command_prefix=config.get('command_prefix'))

server_info = server_info(config)

mm_player_list = []


@client.event
async def on_ready():
    client.loop.create_task(refresh_server_info())
    client.loop.create_task(check_mm_state())
    print('Bot logged in as {0.user}'.format(client))

# !server - show server info embed
@client.command()
async def server(ctx):  
    server_info.get()
    status = server_info.curr_map + ' | ' + server_info.players  
    embedVar = discord.Embed(title=server_info.server_name, color=0x00ff00) 
    if(len(config.get('custom_thumb')) > 0):
        embedVar.set_thumbnail(url=config.get('custom_thumb'))
    map_banner = config['map_banner'].get(server_info.curr_map, None)
    if(map_banner):
        if(len(map_banner) > 0):
            embedVar.set_image(url=map_banner)
    embedVar.add_field(name='\u200b', value=server_info.connect_link, inline=False)
    embedVar.add_field(name='Map', value=server_info.curr_map, inline=True)
    embedVar.add_field(name='Players', value=server_info.players, inline=True)
    embedVar.add_field(name='Ping', value=server_info.ping, inline=True)
    embedVar.add_field(name='\u200b', value='\u200b', inline=False)
    for player in server_info.player_list:
            playerscore =  str(player.score) + ' Kills'
            embedVar.add_field(name=player.name, value=playerscore, inline=True)    
    await client.change_presence(activity=discord.Game(name=status))    
    await ctx.send(embed=embedVar)

# !ip - get connect link to server
@client.command()
async def ip(ctx):
    await ctx.send(server_info.connect_link)

@client.command()
async def servercmds(ctx):
    embedVar = discord.Embed(title='CS:GO server commands', color=0x0000ff)
    for command in config['server_commands']:
        embedVar.add_field(name=command, value=config['server_commands'].get(command, 'Unknown'), inline=False)
    await ctx.send(embed=embedVar)

# !mminfo - show players searching for teammates
@client.command()
async def mminfo(ctx):
    title = 'These users are searching for teammates!'
    embedVar = discord.Embed(title=title, color=0xff0000)
    embedVar.add_field(name='Players searching:', value='\u200b', inline=False)
    
    for player in mm_player_list:
        time_diff = str(int(player.time_diff.total_seconds() / 60) % 60) + ' min'
        embedVar.add_field(name=player.author.name, value=time_diff, inline=True)

    await ctx.send(embed=embedVar)

# !mmsearch - search for matchmaking teammates
@client.command()
async def mmsearch(ctx):
    
    embedVar = discord.Embed(title='Players searching:', color=0xff0000)
    if player_exists(x for x in mm_player_list if x.author.id == ctx.message.author.id):
        for player in mm_player_list:
            # renew timestamp for already existing player
            if player.author.id == ctx.message.author.id:
                player.init_time = datetime.now()
                player.time_diff = timedelta(seconds=0)
    else:
        # register new player
        mm_player_list.append(mm_player(ctx.message.author))
    
    for player in mm_player_list:
        time_diff = str(int(player.time_diff.total_seconds() / 60) % 60) + ' min'
        embedVar.add_field(name=player.author.name, value=time_diff, inline=True)

    mm_notify_name = config.get('mm_notify_role', None)
    if mm_notify_name:
        mm_notify_role = [r for r in ctx.guild.roles if r.name == mm_notify_name][0]
        title = mm_notify_role.mention + ' ' + ctx.message.author.name + ' is searching for teammates!'
        await ctx.send(title)

    await ctx.send(embed=embedVar)

# !mmstop - stop searching for matchmaking teammates
@client.command()
async def mmstop(ctx):
    title = ctx.message.author.name + ' stopped searching for teammates :('
    embedVar = discord.Embed(title=title, color=0xff0000)
    embedVar.add_field(name='Players searching:', value='\u200b', inline=False)
    for player in mm_player_list:
        if player.author.id == ctx.message.author.id:
                mm_player_list.remove(player)

    for player in mm_player_list:
        time_diff = str(int(player.time_diff.total_seconds() / 60) % 60) + ' min'
        embedVar.add_field(name=player.author.name, value=time_diff, inline=True)

    await ctx.send(embed=embedVar)

# !about
@client.command()
async def about(ctx):
    embedVar = discord.Embed(title='discord-csgo-bot', color=0x00ff00)
    embedVar.add_field(name='gitHub', value='https://github.com/pd00m/discord-csgo-bot', inline=False)
    await ctx.send(embed=embedVar)

client.run(config.get('token'))




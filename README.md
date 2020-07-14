# discord-csgo-bot
A simple discord bot for getting the status of a CSGO server via command

## Installing
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
## Configuration
You will need to create a file named config.json in the base directory.

server_ip: server ip  
server_port: server port  
custom_thumb: custom thumbnail path for the server status embed, leave empty if you don't want it  
token: your discord api token  
command_prefix: command prefix.  
refresh_time: how often should the bot refresh the server status in the background in seconds  
mm_nofity_role: the role that gets a ping whenever players start searching for matchmaking partners  
mm_status_reset_minutes: maximum idle time until a player stops searching automatically  
map_banner[list]: map banner image urls for !server embed. If a map banner is not exisiting, the embed banner will stay blank  
server_commands[list]: csgo server commands that are availiable  

### Example config
```json
{
    "server_ip": "127.0.0.1",
    "server_port": 27015,
    "custom_thumb": "https://test.com/images/test.png",
    "token" : "YOUR_DISCORD_API_TOKEN",
    "command_prefix" : "!",
    "refresh_time" : 600,
    "mm_notify_role": "YOUR_DISCORD_NOTIFY_ROLE",
    "mm_status_reset_minutes" : 30,
    "map_banner" : 
    {
        "de_aztec" : "https://url.com/aztec.png",
        "fy_pool_day" : "https://url.com/fy_pool_day.png"
    },
    "server_commands":
    {
        "!soundlist" : "Lists all playable custom sounds",
        "!admin" : "SourceMod admin menu",
        "!quake" : "QuakeSounds settings",
        "!rank" : "Shows your rank on the server",
        "!votemap" : "Start a map vote"
    }
}
```

## Usage
```
python3 main.py
```

### Commands
!server: show server info embed  
!ip: get connect link to server  
!mminfo: show currently searching players  
!mmsearch: enter matchmaking search queue  
!mmstop: exit matchmaking queue  

![Response from bot](response.png?raw=true "response")
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

**server_ip:** server ip  
**server_port:** server port  
**custom_thumb:** custom thumbnail path for the server status embed, leave empty if you don't want it  
**token:** your discord api token  
**command_prefix:** command prefix.  
**refresh_time:** how often should the bot refresh the server status in the background in seconds  
**mm_nofity_role:** the role that gets a ping whenever players start searching for matchmaking partners  
**mm_status_reset_minutes:** maximum idle time until a player stops searching automatically  
**map_banner[list]:** map banner image urls for !server embed. If a map banner is not exisiting, the embed banner will stay blank  
**server_commands[list]:** csgo server commands that are availiable  

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

### run as systemd service
/etc/systemd/system/discordbot.service
```
[Unit]
Description=Discord csgo bot
After=syslog.target

[Service]
Type=simple
WorkingDirectory=~/discord-csgo-bot
ExecStart=~/discord-csgo-bot/env/bin/python3 ~/discord-csgo-bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
*systemd need the full path to your python binary if you're using a venv!* 

Reload daemon and start service manually:
```
sudo systemctl daemon-reload
sudo systemctl start discordbot.service
```

To make it start automatically after reboot:
```
sudo systemctl enable discordbot.service
```

Check the current ouput of the service:
```
sudo journalctl -u discordbot.service
```

### Commands
**!server:** show server info embed  
**!ip:** get connect link to server  
**!mminfo:** show currently searching players  
**!mmsearch:** enter matchmaking search queue  
**!mmstop:** exit matchmaking queue  

![Response from bot](response.png?raw=true "response")
*Respone after sending !server command*

## Common issues

### The bot is not responding to any commands
Check the bot privileges for that channel. It has to be able to read and send messages for that particular channel

### !server is not showing player names and score
Check if server cvar `host_players_show` is set to 2, otherwise all player names are hidden by the server

### The ping is incorrect
The bot itself is pinging the server so this depends on the internet connection the bot has

### The connect link is not doing anything
If you have a password protected server, for some people the password input window from steam is not focussing and pops up in the background sometimes

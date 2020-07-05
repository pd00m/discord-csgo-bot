# discord-csgo-bot
a simple bot for discord for getting the server status via command

## Installing
```
python3 -m venv env
source env/bin activate
pip3 install -r requirements.txt
```
### Configuration
You will need to create a file named config.json in the base directory.

server_ip: server ip
server_port: server port
custom_thumb: custom thumbnail for the server status embed
token: your discord api token
command_prefix: command prefix.
refresh_time: how often should the bot refresh the server status in the background in seconds
```json
{
    "server_ip": "127.0.0.1",
    "server_port": 27015,
    "custom_thumb": "",
    "token" : "YOUR_DISCORD_API_TOKEN",
    "command_prefix" : "!",
    "refresh_time" : 600
}
```

### Usage
```
python3 main.py
```

Type in !server in one of the channels that the bot has access to

![Response from bot](response.png?raw=true "response")
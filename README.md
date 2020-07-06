# discord-csgo-bot
a simple discord bot for getting the status of a CSGO server via command 

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
custom_thumb: custom thumbnail path for the server status embed, leave empty if you don't want it  
custom_banner: custom banner path for the server status embed, leave empty if you don't want it  
token: your discord api token  
command_prefix: command prefix.  
refresh_time: how often should the bot refresh the server status in the background in seconds  


```json
{
    "server_ip": "127.0.0.1",
    "server_port": 27015,
    "custom_thumb": "https://test.com/images/test.png",
    "custom_banner": "https://test.com/images/test.png",
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
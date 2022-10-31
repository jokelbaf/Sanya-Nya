![Image](https://media.discordapp.net/attachments/1029785771839864852/1029785831180877864/banner.gif) 

![](https://img.shields.io/badge/bot_version-v1.0.3-%23ebd8c3?style=for-the-badge&logo=python&logoColor=white)  ![](https://img.shields.io/badge/bot_language-russian_/_english-%23c5d9d7?style=for-the-badge)
****

This is a repo with source for Sanya-nya discord bot. It plays music from YouTube and works both on slash and prefixed commands.

You can invite the official version of the bot [here](https://discord.com/api/oauth2/authorize?client_id=1028248893600841748&permissions=2184563712&scope=bot%20applications.commands).

# Commands
List of all bot's commands and their description on russian.

- `ping` - Current Sanya's ping
- `help` - List of all bot commands and it's prefix
- `play` - Play/Add song to the queue
- `stop` - Stop player, disconnect from VC
- `loop` - Loop current track
- `skip` - Skip current track
- `queue` - View current track queue
- `pause` - Pause player playback
- `status` - Info about current Bot status
- `volume` - Change player volume
- `resume` - Resume playback
- `replay` - Replay current track
- `previous` - Play previous track

# Hosting bot by yourself
This bot is completely ready to be hosted on Railway: 
1. Clone this repo.
2. Fill `Config.py` with your credentials.
3. Create an application on [Discord Developer Portal](https://discord.com/developers/applications).
4. Invite your newly created bot to your server with url which you can generate on application settings page.
5. Go to [railway.app](https://railway.app), connect your GitHub account and deploy your cloned repo.
6. Set your bot token as an enviromental variable named `BOT_TOKEN` on Railway.
7. You are done!

**Important:** If you are going to host this bot by yourself, I highly recommend to use **your** lavalink server hosted by **you** or on a **hosting**. I'm too lazy to look for ways of doing it but you should definitely come up with something.

# Additional info
- Remember that bots that play music from YouTube violate discord rules and will never be verified by discord, and may even be banned.

- This bot is just a fun project, it contains the code for one of Ari's old modules, which was abandoned due to an update to the discord rules.

- If you found a bug you can create an issue and if I have time I will look through it. Pull requests are also welcome.

- To change language of the Bot, go to `Config.py, line 9` and change it to either `ru` or `en`. You can actually implement database to change language per guild/user but I'm too lazy for this shit.

# Links
- **[License](https://github.com/RealSosiso4ka/Sanya-Nya/blob/master/LICENSE)** 
- **[Requirements](https://github.com/RealSosiso4ka/Sanya-Nya/blob/master/requirements.txt)**

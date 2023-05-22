<img src="https://github.com/JokelBaf/Sanya-Nya/assets/60827680/e9c74055-d5b9-4c13-805a-8bd252fb1eb6">

![](https://img.shields.io/badge/bot_version-v1.1.0-%23ebd8c3?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/bot_languages-russian_/_english-%23c5d9d7?style=for-the-badge) ![](https://img.shields.io/badge/maintained-yes-%d4a36e?style=for-the-badge) 
****

This is a repo with source code for Sanya-nya Discord bot. It plays music from YouTube and works both on slash and prefixed commands. You can invite the official version of Sanya-nya [here](https://discord.com/api/oauth2/authorize?client_id=1028248893600841748&permissions=2184563712&scope=bot%20applications.commands). Or host your own instance of Sanya-nya with the button below:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/W-FL4b?referralCode=XzPSfV)

# Overview
<img src="https://github.com/JokelBaf/Sanya-Nya/assets/60827680/215393c3-7241-4ff8-bf91-248eb1e09a89" width="900">

# Screenshots
<img src="https://github.com/JokelBaf/Sanya-Nya/assets/60827680/ba328ccc-5b35-4976-acf0-1d4628147a01" width="450">
<img src="https://github.com/JokelBaf/Sanya-Nya/assets/60827680/92bdab02-43db-402d-a3da-c409338a40d2" width="450">

# Commands
List of all bot's commands and their description.

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
- `language` - Change Bot's language for yourself

# Hosting bot by yourself
This bot is completely ready to be hosted on Railway:
1. Click `Deploy on Railway` button above.
2. Follow instructions to deploy the bot to Railway.
3. Remember to set environmental variables like `BOT_TOKEN`, `LAVALINK_URI` to yours.
4. If you don't have a Discord bot you can create it on [Discord Developer Portal](https://discord.com/developers/applications).
5. Remember to add your bot to your server. Invite url can be generated on application settings page.
6. Now, when your bot is deployed and all variables are set, you need to set custom build command ([here](https://github.com/JokelBaf/Sanya-Nya/issues/5#issuecomment-1556309834) is why):
  - Go to your railway project **Settings**.
  - Find field named **Build command**.
  - Paste the following text there:
  ```
  pip uninstall -y discord.py && pip uninstall -y py-cord && pip install py-cord
  ```
7. That's all! Your bot should now be up and running.

**Important:** If you are going to host this bot by yourself, I highly recommend to use **your** lavalink server hosted by **you** or on a **hosting**. I'm too lazy to look for ways of doing it but you should definitely come up with something.

# Additional info
- Remember that bots that play music from YouTube violate discord rules and will never be verified by Discord, and may even be banned.

- This bot is just a fun project, it contains the code from one of my other bot's old modules, which was abandoned due to an update to the Discord rules.

- If you found a bug you can create an issue and if I have time I will look through it. Pull requests are also welcome.

# Links
- **[License](https://github.com/RealSosiso4ka/Sanya-Nya/blob/master/LICENSE)** 
- **[Requirements](https://github.com/RealSosiso4ka/Sanya-Nya/blob/master/requirements.txt)**

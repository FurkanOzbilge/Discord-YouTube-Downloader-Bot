# Discord YouTube Downloader Bot

![Project Logo](images/logo.png)

This project is a Discord bot that saves YouTube videos to Mega cloud storage.

## Features

- Detects YouTube video links in Discord channel messages
- Downloads YouTube videos
- Uploads downloaded videos to Mega cloud account

## Requirements

- Python 3.10+
- discord.py
- pytubefix
- mega.py

## Installation

First, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Configuration
```json
{
    "discord_token": "YOUR_DISCORD_TOKEN",
    "mega_mail": "YOUR_MEGA_EMAIL",
    "mega_password": "YOUR_MEGA_PASSWORD"
}
```


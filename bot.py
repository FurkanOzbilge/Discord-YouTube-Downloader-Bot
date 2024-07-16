import discord
from pytubefix import YouTube
import os
import random
from mega import Mega
import json
from datetime import date
import re

with open('settings.json', 'r', encoding='utf-8') as dosya:
    settings = json.load(dosya)

mega = Mega()
m = mega.login(settings.get("mega_mail"), settings.get("mega_password"))

intents1 = discord.Intents.default()
intents1.message_content = True

client = discord.Client(intents=intents1)

def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_match = re.match(youtube_regex, url)
    return youtube_match

def VideoSave(InputLink, id):
    if not is_valid_youtube_url(InputLink):
        print("Geçersiz YouTube linki.")
        return None

    try:
        yt = YouTube(InputLink)
        yt.check_availability()
        print("Video doğrulandı.")
    except Exception as e:
        print("Böyle bir video yok.")
        return None

    print(f"Kullanıcı ID: {id} \nVideo URL: {InputLink} \nVideo Başlığı: {yt.title} \nVideo Uzunluğu: {yt.length}")
    if yt.length > 3600:
        print("1 Saatten uzun video!")
        return None
    else:
        out_file = yt.streams.first().download()
        print("İndirme Başarılı!")
        date1 = date.today().strftime("%d_%m_%Y")
        file_name = f"{id}-{date1}-{random.random()}.mp4"
        os.rename(out_file, file_name)
        upload_file = m.upload(file_name)
        file = m.find(file_name)
        link = m.get_link(file)
        print(link)
        os.remove(file_name)
        return link

def VideoInformation(VideoURL):
    Informations = []
    yt = YouTube(VideoURL)
    title = str(yt.title)
    channel = str(yt.channel_url)
    thumbnail = yt.thumbnail_url
    Informations += VideoURL, title, channel, thumbnail
    return Informations

@client.event
async def on_ready():
    print(f"{client.user} olarak giriş yapıldı.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!test"):
        await message.channel.send("Hi!")
    if message.content.startswith("!save") or message.content.startswith("!kaydet"):
        link = message.content.split(" ")[1]
        id = message.author.id
        sent_message = await message.reply("## Video indiriliyor... ⏳")
        print("---------------------------------------------------------------")
        UploadLink = VideoSave(link, id)
        if UploadLink is None:
            await sent_message.edit(content="## Video indirilemedi. Geçersiz link, video bulunamadı veya video çok uzun. ❌")
            print("---------------------------------------------------------------")
            return
        Informations = VideoInformation(link)
        await sent_message.edit(
            content="## İşlem tamamlandı! ✅\n> # DM Kutunuzu kontrol edebilirsiniz.")
        await message.author.send(
            f"# Videonuz Hazır!\n> Video URL: **<{Informations[0]}>**\n> Video Başlığı: **{Informations[1]}**\n> Kanal: **{Informations[2]}**\n> ## Mega Linki: <{UploadLink}>")
        print("---------------------------------------------------------------")
        return

client.run(settings.get("discord_token"))

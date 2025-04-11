#Created for Devansh — the G.O.A.T.

from telethon 
import TelegramClient, events, Button from telethon.sessions 
import StringSession 
import random 
import asyncio 
import requests 
import base64 
import json 
import time 
import os 
import datetime from dotenv 
import load_dotenv

load_dotenv()

#Session and API credentials from environment

API_ID = int(os.getenv("API_ID")) API_HASH = os.getenv("API_HASH") SESSION = os.getenv("SESSION")

bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

#Globals

alive_pic = None is_afk = False afk_reason = "I am AFK."

@bot.on(events.NewMessage(pattern=r"^.alive$")) async def alive(event): pic = alive_pic if alive_pic else "https://telegra.ph/file/e4d9e82a3e9f758a62ff2.jpg" await bot.send_file( event.chat_id, file=pic, caption=f"Userbot is alive!\nOwner: @my_intrusive_thought_won", buttons=[[Button.inline("Commands", data=b"cmds")]], reply_to=event.id )

@bot.on(events.CallbackQuery(data=b"cmds")) async def command_buttons(event): await event.edit( "COMMAND MENU\nTap buttons to see categories:", buttons=[ [Button.inline("Fun", b"fun"), Button.inline("Utility", b"util")], [Button.inline("AFK", b"afk"), Button.inline("Alive", b"alive")], [Button.inline("Back", b"back")] ] )

@bot.on(events.CallbackQuery(data=b"fun")) async def fun_cmds(event): await event.edit( "Fun Commands\n.afk, .lol, .cry, .tableflip, .hack, .type, .joke", buttons=[Button.inline("Back", b"cmds")] )

@bot.on(events.CallbackQuery(data=b"util")) async def util_cmds(event): await event.edit( "Utility Commands\n.id, .ping, .time, .weather <city>, .ss <url>", buttons=[Button.inline("Back", b"cmds")] )

@bot.on(events.NewMessage(pattern=r"^.setalive$")) async def set_alive(event): if event.reply_to_msg_id: reply = await event.get_reply_message() if reply.photo: path = await bot.download_media(reply) global alive_pic alive_pic = path await event.reply("Alive picture updated!") else: await event.reply("Reply to a photo to set it as alive.") else: await event.reply("Reply to a photo to set it as alive.")

@bot.on(events.NewMessage(pattern=r"^.afk(?:\s+(.*))?$")) async def set_afk(event): global is_afk, afk_reason is_afk = True reason = event.pattern_match.group(1) if reason: afk_reason = reason await event.reply(f"AFK activated. Reason: {afk_reason}")

@bot.on(events.NewMessage()) async def auto_afk_reply(event): if is_afk and event.mentioned: await event.reply(afk_reason)

@bot.on(events.NewMessage(pattern=r"^.command$")) async def show_command(event): await event.respond( "Welcome to Devansh's userbot!\nChoose a category:", buttons=[[Button.inline("Commands", data=b"cmds")]] )

#Add more commands below as needed

@bot.on(events.NewMessage(pattern=r"^.ping$")) async def ping(event): start = time.time() msg = await event.reply("Pinging...") end = time.time() await msg.edit(f"Pong! {round((end - start) * 1000)}ms")

@bot.on(events.NewMessage(pattern=r"^.joke$")) async def joke(event): j = requests.get("https://v2.jokeapi.dev/joke/Any?format=txt").text await event.reply(j)

@bot.on(events.NewMessage(pattern=r"^.id$")) async def user_id(event): await event.reply(f"Your user ID is: {event.sender_id}")

@bot.on(events.NewMessage(pattern=r"^.time$")) async def time_cmd(event): current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') await event.reply(f"Current time: {current_time}")

@bot.on(events.NewMessage(pattern=r"^.weather(?:\s+(.+))?$")) async def weather(event): city = event.pattern_match.group(1) if city: url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric" response = requests.get(url).json() if response['cod'] == 200: temp = response['main']['temp'] weather_desc = response['weather'][0]['description'] await event.reply(f"Weather in {city}: {temp}°C, {weather_desc}") else: await event.reply(f"Could not get weather data for {city}") else: await event.reply("Please provide a city name.")

@bot.on(events.NewMessage(pattern=r"^.ss(?:\s+(.+))?$")) async def ss(event): url = event.pattern_match.group(1) if url: await event.reply(f"Screenshot for {url}.") else: await event.reply("Please provide a URL.")

#Start bot

print("\n[INFO] Userbot is starting...") bot.start() bot.run_until_disconnected()


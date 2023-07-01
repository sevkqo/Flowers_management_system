
import nest_asyncio
nest_asyncio.apply()
import discord
from discord.ext import tasks, commands
import datetime
import sys
import logging
import src.logger_configuration as logger_configuration

sys.path.insert(0, '/home/sevkqo/flowers_management/hmi')
from website.models import Flowers_data

logger_configuration.main('INFO')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

#part of day when bot can send notifications
publication_time = [
    datetime.time(hour=16, minute=0, second=0, tzinfo=datetime.timezone.utc)
]

class DiscordBot():
    def __init__(self):
        self.TOKEN = "MTEwNTk1NDU1MTM5MzE2NTQxMg.GHujeq.2dRYL7VYroe7pI8iAN4aAF-EQeyjliFLEh-QJA"
        self.channel = 951538486710788168

    def run(self):
        logging.info(f'starting discord bot thread...')
        bot.run(self.TOKEN)

@tasks.loop(time = publication_time)
async def on_message():
    flower_1 = Flowers_data.objects.latest('measurement_date').flower_1
    flower_2 = Flowers_data.objects.latest('measurement_date').flower_2
    flower_3 = Flowers_data.objects.latest('measurement_date').flower_3
    channel = bot.get_channel(951538486710788168) #connect with channel on discord
    await channel.send(f'Hi! Actual soil moisture values:\nFlower 1: {flower_1}%,\nFlower 2: {flower_2}%,\nFlower 3: {flower_3}%.')

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')
    on_message.start()




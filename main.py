import time
import datetime
from threading import Thread
import os
import sys
import django
import logging
from communication.MCP3208 import MCP3208_sensor
import src.logger_configuration as logger_configuration

'''configure django server setup'''
sys.path.insert(0, '/home/sevkqo/flowers_management/hmi')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hmi.settings'
django.setup()
from website.models import Flowers_data
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from discord_bot.discord_bot import DiscordBot

'''logger configuration'''
logger_configuration.main('INFO')

class Supervisor():
    def __init__(self):
        self.spi0_adc = MCP3208_sensor()
        self.django_path = "/home/sevkqo/flowers_management/hmi"

    '''django server thread'''
    def django_run(self):
        os.chdir(self.django_path)
        os.system("python3 manage.py runserver 0.0.0.0:8000")

    '''configure django server thread'''
    def django_thread(self):
        self.django_server = Thread(target = self.django_run)
        self.django_server.start()

    '''discord bot thread'''
    def discord_bot_run(self):
        self.discord_bot = DiscordBot()
        self.discord_bot.run()

    '''configure discord bot thread'''
    def discord_bot_thread(self):
        self.discord_client = Thread(target = self.discord_bot_run)
        self.discord_client.start()

    '''read data from sensors'''
    def read_all_data(self):
        while True: #TODO its time to make it dependent from connection to network or something like that.
            self.adc_0 = self.spi0_adc.calculate_value(0)
            logging.info(f'adc0 value (soil moisture 1st flower): {self.adc_0}')
            self.adc_1 = self.spi0_adc.calculate_value(1)
            logging.info(f'adc1 value (soil moisture 2nd flower): {self.adc_1}')
            self.adc_2 = self.spi0_adc.calculate_value(2)
            logging.info(f'adc2 value (soil moisture 3rd flower): {self.adc_2}')
            self.sql_insert()
            time.sleep(3600)

    '''insert data to postgresql'''
    def sql_insert(self):
        insert = Flowers_data(measurement_date=datetime.datetime.now(datetime.timezone.utc), flower_1=self.adc_0, flower_2=self.adc_1, flower_3=self.adc_2)
        insert.save()
        logging.info(f'getting data into database...')

    '''start threads and local functions'''
    def run(self):
        self.django_thread()
        self.discord_bot_thread()
        self.read_all_data()

if __name__ == "__main__":
    supervisor_app = Supervisor()
    supervisor_app.run()

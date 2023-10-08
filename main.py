import time
import datetime
import os
import sys
import django
import logging
from threading import Thread
from communication.MCP3208 import MCP3208_sensor
from communication.I2C import I2C_sensor
import src.logger_configuration as logger_configuration
from src.postgresql_log import Sensors_data

from discord_bot.discord_bot import DiscordBot

'''logger configuration'''
logger_configuration.main('INFO')

class Supervisor():
    def __init__(self):
        self.spi0_adc = MCP3208_sensor()
        self.i2c_sensors = I2C_sensor()
        self.sensors_data = Sensors_data()
        self.django_path = "/home/sevkqo/flowers_management/hmi"
        self.lifetime = 0
        self.sql_insert_delay = 300 # time in [s] to get properly data from sensors
        self.actual_datetime_sql = 0
        self.flower_1_soil_moisture = 0
        self.flower_2_soil_moisture = 0
        self.flower_3_soil_moisture = 0
        self.brightness = 0
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.voc = 0

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

    '''start threads and local functions'''
    def run(self):
        self.django_thread()
        self.discord_bot_thread()
        self.sensors_data.sql_django_configuration()
        self.sensors_data.lifetime = datetime.datetime.now()
        self.sensors_data.read_all_data()

if __name__ == "__main__":
    supervisor_app = Supervisor()
    supervisor_app.run()
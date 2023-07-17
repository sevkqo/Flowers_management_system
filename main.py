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

'''configure django server setup'''
sys.path.insert(0, '/home/sevkqo/flowers_management/hmi')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hmi.settings'
django.setup()
from website.models import Flowers_data, Environment_data
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from discord_bot.discord_bot import DiscordBot

'''logger configuration'''
logger_configuration.main('INFO')

class Supervisor():
    def __init__(self):
        self.spi0_adc = MCP3208_sensor()
        self.i2c_sensors = I2C_sensor()
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

    '''read data from sensors'''
    def read_all_data(self):
        while True: #TODO its time to make it dependent from connection to network or something like that.
            self.actual_datetime_sql = datetime.datetime.now(datetime.timezone.utc)
            self.flower_1_soil_moisture = self.spi0_adc.soil_moisture_calculate_value(0)
            logging.info(f'adc0 value (soil moisture 1st flower): {self.flower_1_soil_moisture} %')
            self.flower_2_soil_moisture = self.spi0_adc.soil_moisture_calculate_value(1)
            logging.info(f'adc1 value (soil moisture 2nd flower): {self.flower_2_soil_moisture} %')
            self.flower_3_soil_moisture = self.spi0_adc.soil_moisture_calculate_value(2)
            logging.info(f'adc2 value (soil moisture 3rd flower): {self.flower_3_soil_moisture} %')
            self.brightness = self.spi0_adc.brightness_calculate_value(3)
            logging.info(f'adc3 value (brightness): {self.brightness} %')
            self.temperature = self.i2c_sensors.get_temperature()
            logging.info(f'temperature value: {self.temperature} C')
            self.humidity = self.i2c_sensors.get_humidity()
            logging.info(f'humidity value: {self.humidity} %')
            self.pressure = self.i2c_sensors.get_pressure()
            logging.info(f'pressure value: {self.pressure} hPa')
            self.voc = self.i2c_sensors.get_voc_value()
            logging.info(f'voc value: {self.voc} VOC index')
            logging.info(f'{datetime.datetime.now() - self.lifetime}')
            if datetime.datetime.now() - self.lifetime > datetime.timedelta(seconds = self.sql_insert_delay):
                self.sql_insert()
            time.sleep(10) #TODO change to hourly

    '''insert data to postgresql'''
    def sql_insert(self):
        insert_flowers_data = Flowers_data(measurement_date=self.actual_datetime_sql, flower_1=self.flower_1_soil_moisture, flower_2=self.flower_2_soil_moisture, flower_3=self.flower_3_soil_moisture)
        insert_environment_data = Environment_data(measurement_date=self.actual_datetime_sql, brightness = self.brightness, temperature=self.temperature, humidity=self.humidity, pressure=self.pressure, voc = self.voc)
        insert_flowers_data.save()
        insert_environment_data.save()
        logging.info(f'getting data into database...')

    '''start threads and local functions'''
    def run(self):
        self.django_thread()
        self.discord_bot_thread()
        self.lifetime = datetime.datetime.now()
        self.read_all_data()

if __name__ == "__main__":
    supervisor_app = Supervisor()
    supervisor_app.run()

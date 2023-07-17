import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_sgp40
import src.logger_configuration as logger_configuration

logger_configuration.main('INFO')

class I2C_sensor():
    def __init__(self):
        self.i2c = board.I2C()
        self.bme280_sensor = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)
        self.sgp40_sensor = adafruit_sgp40.SGP40(self.i2c)
    
    def get_temperature(self):
        return round(self.bme280_sensor.temperature, 1)
    
    def get_humidity(self):
        return round(self.bme280_sensor.humidity, 1)
    
    def get_pressure(self):
        return round(self.bme280_sensor.pressure, 1)
    
    def get_voc_value(self):
        return self.sgp40_sensor.measure_index(temperature = self.get_temperature(), relative_humidity = self.get_humidity())
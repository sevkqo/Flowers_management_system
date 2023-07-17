'''File for retrieving data by SPI communaction'''
import spidev
import logging
import src.logger_configuration as logger_configuration

logger_configuration.main('INFO')

class MCP3208_sensor():
    def __init__(self):
        self.vref = 3.3
        '''SPI configuration'''
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 1200000

    def get_data(self, channel):
        self.raw_data = self.spi.xfer2([ 6 | (channel&4) >> 2, (channel&3)<<6, 0])

    def soil_moisture_calculate_value(self, channel):
        self.get_data(channel)
        self.value = (((self.raw_data[1]&15) << 8) + self.raw_data[2])*self.vref / 4096
        return round((100 - (self.value * 100 / self.vref)) / 0.72, 2)
    
    def brightness_calculate_value(self, channel):
        self.get_data(channel)
        self.value = (((self.raw_data[1]&15) << 8) + self.raw_data[2])*self.vref / 4096
        return round((self.value * 100 / self.vref), 2)
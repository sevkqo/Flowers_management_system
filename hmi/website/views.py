from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.insert(0, '/home/sevkqo/flowers_management')
from communication.MCP3208 import MCP3208_sensor
from communication.I2C import I2C_sensor
django_SPI = MCP3208_sensor()
django_I2C = I2C_sensor()

# Create your views here.
def main_page(request):
    return render(request, 'main_page.html', {'flower_1': django_SPI.soil_moisture_calculate_value(0),
     'flower_2': django_SPI.soil_moisture_calculate_value(1),
     'flower_3': django_SPI.soil_moisture_calculate_value(2),
     'brightness': django_SPI.brightness_calculate_value(3),
     'temperature': django_I2C.get_temperature,
     'humidity': django_I2C.get_humidity,
     'pressure': django_I2C.get_pressure,
     'VOC': django_I2C.get_voc_value,
     'base': 'base.html' })

def diagrams(request):
    return render(request, 'diagrams.html')
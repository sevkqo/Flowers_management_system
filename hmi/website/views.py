from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.insert(0, '/home/sevkqo/flowers_management')
from communication.MCP3208 import MCP3208_sensor
django_soil_moistures = MCP3208_sensor()
# Create your views here.
def test(request):
    return render(request, 'test.html', {'flower_1': django_soil_moistures.calculate_value(0),
     'flower_2': django_soil_moistures.calculate_value(1),
     'flower_3': django_soil_moistures.calculate_value(2)}) 
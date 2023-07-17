from django.db import models

# Create your models here.
class Flowers_data(models.Model):
    measurement_date = models.DateTimeField()
    flower_1 = models.FloatField(max_length=80)
    flower_2 = models.FloatField(max_length=80)
    flower_3 = models.FloatField(max_length=80)

    def __str__(self):
        return str(self.measurement_date)
    
class Environment_data(models.Model):
    measurement_date = models.OneToOneField(
        Flowers_data,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    measurement_date = models.DateTimeField()
    brightness = models.FloatField(max_length=80)
    temperature = models.FloatField(max_length=80)
    humidity = models.FloatField(max_length=80)
    pressure = models.FloatField(max_length=80)
    voc = models.IntegerField()
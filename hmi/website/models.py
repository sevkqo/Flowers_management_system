from django.db import models

# Create your models here.
class Flowers_data(models.Model):
    measurement_date = models.DateTimeField()
    flower_1 = models.FloatField(max_length=80)
    flower_2 = models.FloatField(max_length=80)
    flower_3 = models.FloatField(max_length=80) 
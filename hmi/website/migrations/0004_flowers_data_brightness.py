# Generated by Django 4.2.1 on 2023-07-10 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_rename_soil_moisture_flowers_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowers_data',
            name='brightness',
            field=models.FloatField(default=0, max_length=80),
            preserve_default=False,
        ),
    ]

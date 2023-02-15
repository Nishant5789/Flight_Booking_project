# Generated by Django 4.0.1 on 2023-01-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0009_flight_component_total_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight_component',
            name='id',
        ),
        migrations.AddField(
            model_name='flight_component',
            name='Temparal_ID',
            field=models.IntegerField(default=100000, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]

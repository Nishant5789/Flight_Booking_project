# Generated by Django 4.0.1 on 2023-01-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0012_alter_flight_component_airline_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_component',
            name='Temparal_ID',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
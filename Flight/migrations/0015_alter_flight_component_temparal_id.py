# Generated by Django 4.0.1 on 2023-01-22 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flight', '0014_alter_flight_component_temparal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight_component',
            name='Temparal_ID',
            field=models.IntegerField(default=138936735906268186, primary_key=True, serialize=False),
        ),
    ]
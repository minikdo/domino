# Generated by Django 2.1.7 on 2019-04-10 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0004_machine_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='datetime',
            field=models.DateField(null=True),
        ),
    ]
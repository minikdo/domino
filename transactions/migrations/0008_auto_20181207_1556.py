# Generated by Django 2.1.3 on 2018-12-07 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20181207_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterpartyaccount',
            name='account',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinLengthValidator(26), django.core.validators.MaxLengthValidator(26)], verbose_name='numer konta'),
        ),
    ]
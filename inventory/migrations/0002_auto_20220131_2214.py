# Generated by Django 3.2 on 2022-01-31 21:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='item',
            name='net_price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(35000)], verbose_name='cena netto'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(35000)], verbose_name='cena brutto'),
        ),
        migrations.AlterField(
            model_name='make',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='makegroup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

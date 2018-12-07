# Generated by Django 2.1.3 on 2018-12-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20181205_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparty',
            name='city',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='miasto'),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='street',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='ulica'),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='tax_id',
            field=models.CharField(blank=True, max_length=35, null=True, unique=True, verbose_name='NIP'),
        ),
        migrations.AlterField(
            model_name='counterpartyaccount',
            name='comment',
            field=models.CharField(blank=True, max_length=50, verbose_name='komentarz'),
        ),
    ]

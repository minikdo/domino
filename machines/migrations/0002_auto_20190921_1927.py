# Generated by Django 2.2.5 on 2019-09-21 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='serial',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='serial number'),
        ),
        migrations.AlterField(
            model_name='device',
            name='invoice',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='invoice number'),
        ),
    ]

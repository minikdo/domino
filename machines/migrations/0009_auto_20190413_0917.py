# Generated by Django 2.1.7 on 2019-04-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0008_auto_20190410_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
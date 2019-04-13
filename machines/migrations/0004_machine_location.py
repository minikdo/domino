# Generated by Django 2.1.7 on 2019-04-10 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0003_auto_20190410_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='machines.Location'),
        ),
    ]
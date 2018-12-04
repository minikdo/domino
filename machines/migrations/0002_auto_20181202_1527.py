# Generated by Django 2.1.3 on 2018-12-02 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='komp',
        ),
        migrations.AddField(
            model_name='device',
            name='machine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='machines.Machine'),
        ),
    ]

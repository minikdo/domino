# Generated by Django 2.1.3 on 2018-12-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_auto_20181213_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderingaccount',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
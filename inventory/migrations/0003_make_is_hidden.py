# Generated by Django 5.1.4 on 2024-12-23 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_auto_20220131_2214"),
    ]

    operations = [
        migrations.AddField(
            model_name="make",
            name="is_hidden",
            field=models.BooleanField(default=False, verbose_name="ukryte"),
        ),
    ]
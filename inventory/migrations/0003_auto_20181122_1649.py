# Generated by Django 2.1.3 on 2018-11-22 15:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20181114_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name': 'lista remanentów', 'verbose_name_plural': 'lista remanentów'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'remanent', 'verbose_name_plural': 'remanenty'},
        ),
        migrations.AlterModelOptions(
            name='make',
            options={'verbose_name': 'nazwa towaru', 'verbose_name_plural': 'nazwy towarów'},
        ),
        migrations.AlterModelOptions(
            name='makegroup',
            options={'verbose_name': 'grupa towarowa', 'verbose_name_plural': 'grupy towarowe'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': 'adres sklepu', 'verbose_name_plural': 'adresy sklepów'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name': 'jednostka miary', 'verbose_name_plural': 'jednostki miar'},
        ),
        migrations.AlterField(
            model_name='inventory',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(11000)], verbose_name='cena brutto'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(100)], verbose_name='ilość'),
        ),
    ]

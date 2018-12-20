# Generated by Django 2.1.3 on 2018-12-13 17:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_auto_20181207_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='ordering_bank',
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='tax_id',
            field=models.CharField(blank=True, help_text='tylko cyfry', max_length=35, null=True, unique=True, verbose_name='NIP'),
        ),
        migrations.AlterField(
            model_name='counterpartyaccount',
            name='account',
            field=models.CharField(max_length=26, unique=True, validators=[django.core.validators.MinLengthValidator(26), django.core.validators.MaxLengthValidator(26)], verbose_name='numer konta'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='kwota'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='execution_date',
            field=models.IntegerField(verbose_name='data wykonania'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_title',
            field=models.CharField(max_length=150, verbose_name='tytuł'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.TransactionStatus'),
        ),
    ]
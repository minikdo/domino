# Generated by Django 2.1.3 on 2018-12-02 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=34, verbose_name='numer konta')),
                ('comment', models.CharField(max_length=50, verbose_name='komentarz')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'konto bankowe',
                'verbose_name_plural': 'konta bankowe',
            },
        ),
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, null=True, verbose_name='nazwa')),
                ('street', models.CharField(max_length=35, null=True, verbose_name='ulica')),
                ('city', models.CharField(max_length=35, null=True, verbose_name='miasto')),
                ('tax_id', models.CharField(max_length=35, null=True, verbose_name='NIP')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Account', verbose_name='konto')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'kontrahent',
                'verbose_name_plural': 'kontrahenci',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.IntegerField()),
                ('execution_date', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('ordering_bank', models.IntegerField()),
                ('ordering_account', models.CharField(max_length=34)),
                ('counterparty_account', models.CharField(max_length=34)),
                ('ordering_name_address', models.CharField(max_length=150)),
                ('counterparty_name_address', models.CharField(max_length=150)),
                ('counterparty_bank', models.IntegerField()),
                ('order_title', models.CharField(max_length=150)),
                ('transaction_classification', models.IntegerField()),
                ('annotations', models.CharField(max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'transakcja',
                'verbose_name_plural': 'transakcje',
            },
        ),
        migrations.CreateModel(
            name='TransactionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='status')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statusy',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.TransactionStatus'),
        ),
    ]

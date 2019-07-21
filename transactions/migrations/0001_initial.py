# Generated by Django 2.2.3 on 2019-07-21 01:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=35, null=True, verbose_name='nazwa')),
                ('street', models.CharField(blank=True, max_length=35, null=True, verbose_name='ulica')),
                ('city', models.CharField(blank=True, max_length=35, null=True, verbose_name='miasto')),
                ('tax_id', models.CharField(blank=True, help_text='tylko cyfry', max_length=35, null=True, unique=True, verbose_name='NIP')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'kontrahent',
                'verbose_name_plural': 'kontrahenci',
            },
        ),
        migrations.CreateModel(
            name='CounterpartyAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('account', models.CharField(max_length=26, unique=True, validators=[django.core.validators.MinLengthValidator(26), django.core.validators.MaxLengthValidator(26)], verbose_name='numer konta')),
                ('comment', models.CharField(blank=True, max_length=50, verbose_name='komentarz')),
                ('counterparty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.Counterparty', verbose_name='kontrahent')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'konto bankowe',
                'verbose_name_plural': 'konta bankowe',
            },
        ),
        migrations.CreateModel(
            name='OrderingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('comment', models.CharField(blank=True, max_length=30, null=True)),
                ('account', models.CharField(max_length=26, unique=True, validators=[django.core.validators.MinLengthValidator(26), django.core.validators.MaxLengthValidator(26)], verbose_name='numer konta')),
            ],
            options={
                'verbose_name': 'konto własne',
                'verbose_name_plural': 'konta własne',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_type', models.CharField(choices=[('110', 'polecenie przelewu (w tym US i ZUS)'), ('210', 'polecenie zapłaty'), ('510', 'polecenie przelewu SORBNET')], max_length=3)),
                ('execution_date', models.DateField(verbose_name='data wykonania')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='kwota')),
                ('ordering_account_text', models.CharField(default='', max_length=26)),
                ('counterparty_account_text', models.CharField(default='', max_length=26)),
                ('ordering_name_address', models.CharField(default='', max_length=150)),
                ('counterparty_name_address', models.CharField(max_length=150)),
                ('order_title', models.CharField(max_length=140, verbose_name='tytuł')),
                ('transaction_classification', models.CharField(choices=[('51', 'for trans type 110, 120'), ('53', 'Split Payment'), ('01', 'for trans type 210'), ('71', 'for trans type 110 (przelew US)')], max_length=2)),
                ('annotations', models.CharField(max_length=32)),
                ('counterparty_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.CounterpartyAccount')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('ordering_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.OrderingAccount')),
            ],
            options={
                'verbose_name': 'transakcja',
                'verbose_name_plural': 'transakcje',
            },
        ),
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, verbose_name='status')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statusy',
            },
        ),
        migrations.CreateModel(
            name='TransactionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ManyToManyField(to='transactions.Transaction')),
            ],
            options={
                'verbose_name': 'paczka przelewów',
                'verbose_name_plural': 'paczki przelewów',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.TransactionStatus'),
        ),
    ]

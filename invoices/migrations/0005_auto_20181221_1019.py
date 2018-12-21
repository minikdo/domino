# Generated by Django 2.1.3 on 2018-12-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20181220_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='postal_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='kod pocztowy'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issue_place',
            field=models.CharField(choices=[('1', 'Ustroń'), ('2', 'Wisła'), ('3', 'Cieszyn')], default='1', max_length=1, verbose_name='miejsce wydania faktury'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment',
            field=models.CharField(choices=[('1', 'gotówka'), ('2', 'karta'), ('3', 'przelew')], default='1', max_length=1, verbose_name='sposób płatności'),
        ),
    ]
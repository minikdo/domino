# Generated by Django 2.2.3 on 2019-07-21 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=150, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('company', models.CharField(blank=True, max_length=150, null=True)),
                ('invoice', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('FQDN', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('form', models.CharField(blank=True, max_length=50, null=True)),
                ('bios', models.CharField(blank=True, max_length=50, null=True)),
                ('prod', models.CharField(blank=True, max_length=150, null=True)),
                ('vendor', models.CharField(blank=True, max_length=150, null=True)),
                ('OS', models.CharField(blank=True, max_length=150, null=True)),
                ('kernel', models.CharField(blank=True, max_length=150, null=True)),
                ('CPU', models.CharField(blank=True, max_length=150, null=True)),
                ('cores', models.CharField(blank=True, max_length=150, null=True)),
                ('arch', models.CharField(blank=True, max_length=150, null=True)),
                ('mem', models.CharField(blank=True, max_length=250, null=True)),
                ('HDD', models.CharField(blank=True, max_length=250, null=True)),
                ('disk', models.CharField(blank=True, max_length=250, null=True)),
                ('diskfree', models.CharField(blank=True, max_length=250, null=True)),
                ('IPs', models.CharField(blank=True, max_length=350, null=True)),
                ('gateway', models.CharField(blank=True, max_length=250, null=True)),
                ('gate_iface', models.CharField(blank=True, max_length=250, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='machines.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=300)),
                ('device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='machines.Device')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.Machine')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='machines.Location'),
        ),
        migrations.AddField(
            model_name='device',
            name='machine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='device', to='machines.Machine'),
        ),
        migrations.AddField(
            model_name='device',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.DeviceType'),
        ),
    ]

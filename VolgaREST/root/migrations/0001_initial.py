# Generated by Django 3.1.4 on 2021-01-03 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopModel',
            fields=[
                ('token', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=128)),
                ('shop', models.CharField(max_length=25)),
                ('country', models.CharField(max_length=90)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=95, null=True)),
                ('foundation', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(error_messages={'unique': 'Otra tienda usa este email.'}, max_length=125, unique=True)),
                ('password', models.CharField(max_length=75)),
            ],
        ),
    ]

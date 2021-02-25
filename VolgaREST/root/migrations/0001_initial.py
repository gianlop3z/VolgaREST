# Generated by Django 3.1.4 on 2021-02-25 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('name', models.CharField(max_length=65)),
                ('picture', models.CharField(blank=True, max_length=256, null=True)),
                ('username', models.CharField(error_messages={'unique': 'Este nombre de usuario ya fue tomado.'}, max_length=25, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=90)),
                ('city', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=20)),
                ('email', models.EmailField(error_messages={'unique': 'Otro usuario usa este correo.'}, max_length=125, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactNetworksModel',
            fields=[
                ('user', models.OneToOneField(error_messages={'unique': 'Este usuario ya añadió sus redes de contacto.'}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='root.usermodel')),
                ('instagram', models.CharField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=30, null=True, unique=True)),
                ('facebook', models.CharField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=50, null=True, unique=True)),
                ('whatsapp', models.CharField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=15, null=True, unique=True)),
                ('twitter', models.CharField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=15, null=True, unique=True)),
                ('linkedin', models.CharField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=30, null=True, unique=True)),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'Otro usuario ya registró esta cuenta.'}, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('images', models.TextField(max_length=2048)),
                ('product', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=15)),
                ('description', models.TextField(blank=True, max_length=145, null=True)),
                ('tags', models.TextField(blank=True, max_length=500, null=True)),
                ('key', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoritesProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='root.productmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClientsOpinionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=10)),
                ('comment', models.TextField(max_length=125)),
                ('date', models.DateField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

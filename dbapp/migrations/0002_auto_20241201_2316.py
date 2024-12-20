# Generated by Django 3.2 on 2024-12-02 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dbapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.CharField(max_length=6)),
                ('dateregistered', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserProfile',
            },
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.AlterModelOptions(
            name='cardelivery',
            options={},
        ),
        migrations.AlterModelOptions(
            name='notifications',
            options={},
        ),
        migrations.AlterModelOptions(
            name='payments',
            options={},
        ),
        migrations.AlterModelOptions(
            name='reservations',
            options={},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={},
        ),
        migrations.AlterModelOptions(
            name='vehiclefeatures',
            options={},
        ),
        migrations.AlterModelOptions(
            name='vehicles',
            options={},
        ),
    ]

# Generated by Django 3.2 on 2024-12-02 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbapp', '0004_auto_20241202_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='vehicle_images/'),
        ),
    ]

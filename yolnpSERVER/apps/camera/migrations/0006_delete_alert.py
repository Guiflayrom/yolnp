# Generated by Django 4.1.6 on 2023-02-13 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0005_alert'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Alert',
        ),
    ]
# Generated by Django 3.2.15 on 2022-09-09 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='job',
            name='image',
        ),
        migrations.RemoveField(
            model_name='job',
            name='start_date',
        ),
    ]
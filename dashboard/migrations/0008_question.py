# Generated by Django 3.2.15 on 2022-09-25 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('question', models.FileField(null=True, upload_to='')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.provider')),
            ],
        ),
    ]

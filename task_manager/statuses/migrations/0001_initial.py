# Generated by Django 4.1.3 on 2022-11-09 13:27
# flake8: noqa
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='DefaultName')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

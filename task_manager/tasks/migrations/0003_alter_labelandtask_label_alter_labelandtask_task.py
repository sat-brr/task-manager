# Generated by Django 4.1.3 on 2022-11-15 05:47
# flake8: noqa
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0002_labelandtask_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelandtask',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labels.label'),
        ),
        migrations.AlterField(
            model_name='labelandtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-07 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='tasks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_photos', to='tasks.task'),
        ),
    ]

# Generated by Django 4.2.11 on 2025-04-10 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firefighters',
            name='station',
        ),
        migrations.AlterField(
            model_name='firefighters',
            name='rank',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

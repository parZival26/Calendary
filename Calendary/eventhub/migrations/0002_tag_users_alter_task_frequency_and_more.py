# Generated by Django 5.0 on 2023-12-11 01:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventhub', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='frequency',
            field=models.CharField(blank=True, choices=[('daily', 'Diariamente'), ('weekly', 'Semanalmente'), ('monthly', 'Mensualmente'), ('yearly', 'Anualmente')], default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='frequency_detail',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, to='eventhub.tag'),
        ),
    ]

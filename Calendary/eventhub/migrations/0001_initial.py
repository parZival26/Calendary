# Generated by Django 5.0 on 2023-12-05 19:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(default='#FFFFFF', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('due_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('has_frequency', models.BooleanField(default=False)),
                ('frequency', models.CharField(blank=True, choices=[('daily', 'Diariamente'), ('weekly', 'Semanalmente'), ('monthly', 'Mensualmente'), ('yearly', 'Anualmente')], max_length=10, null=True)),
                ('frequency_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('tags', models.ManyToManyField(to='eventhub.tag')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

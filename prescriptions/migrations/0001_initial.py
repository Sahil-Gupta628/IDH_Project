# Generated by Django 4.2.7 on 2025-04-14 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_path', models.CharField(max_length=200)),
                ('extracted_text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('dosage', models.CharField(blank=True, max_length=100, null=True)),
                ('frequency', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('scan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='prescriptions.scan')),
            ],
        ),
    ]

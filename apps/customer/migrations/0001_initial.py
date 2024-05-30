# Generated by Django 5.0.6 on 2024-05-30 15:10

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=2, help_text='1=Active, 2=Inactive', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('score', models.DecimalField(decimal_places=10, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0)])),
                ('preapproved_at', models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.datetime(2024, 5, 30, 15, 10, 51, 993764, tzinfo=datetime.timezone.utc))])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

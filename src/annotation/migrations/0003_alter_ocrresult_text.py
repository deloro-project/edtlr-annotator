# Generated by Django 5.0 on 2024-01-28 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_annotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocrresult',
            name='text',
            field=models.TextField(max_length=8192),
        ),
    ]

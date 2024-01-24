# Generated by Django 5.0 on 2024-01-24 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OcrResult',
            fields=[
                ('page_no', models.IntegerField(primary_key=True, serialize=False)),
                ('image_path', models.CharField(max_length=1024, unique=True)),
                ('text', models.CharField(max_length=4096)),
            ],
        ),
    ]

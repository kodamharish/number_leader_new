# Generated by Django 5.0.6 on 2024-06-29 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator_id',
            field=models.CharField(max_length=15),
        ),
    ]

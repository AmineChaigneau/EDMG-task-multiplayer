# Generated by Django 4.2 on 2023-05-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_calibration_created_at_form_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='reward',
            field=models.IntegerField(default=0),
        ),
    ]

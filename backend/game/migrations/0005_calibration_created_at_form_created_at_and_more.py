# Generated by Django 4.2 on 2023-05-04 16:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_calibration_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='calibration',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='calibration',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='form',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='form',
            name='subject_id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
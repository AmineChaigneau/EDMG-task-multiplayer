# Generated by Django 4.2 on 2023-05-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_remove_round_id_trial_round_subject_id_trial_round_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='subject_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='trial',
            name='subject_id',
            field=models.CharField(max_length=255),
        ),
    ]

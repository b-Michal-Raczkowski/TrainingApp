# Generated by Django 4.2.17 on 2025-01-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="achievements",
            field=models.ManyToManyField(blank=True, to="training.achievement"),
        ),
    ]

# Generated by Django 5.1 on 2024-08-27 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0027_alter_dailyplan_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="dailyplan",
            unique_together=set(),
        ),
    ]

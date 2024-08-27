# Generated by Django 5.1 on 2024-08-27 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0023_alter_dailyplan_unique_together_alter_dailyplan_date"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="dailyplan",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="dailyplan",
            name="date",
            field=models.DateField(),
        ),
        migrations.AlterUniqueTogether(
            name="dailyplan",
            unique_together={("weekly_plan", "date")},
        ),
    ]

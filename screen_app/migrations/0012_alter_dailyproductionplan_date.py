# Generated by Django 5.0.2 on 2024-08-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screen_app', '0011_dailyproductionplan_assembly_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyproductionplan',
            name='date',
            field=models.DateField(),
        ),
    ]

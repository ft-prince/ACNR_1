# Generated by Django 5.0.6 on 2024-08-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0016_productionplan_assembly_line_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailyproductionplan",
            name="qty_actual",
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name="productionplan",
            name="qty_actual",
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

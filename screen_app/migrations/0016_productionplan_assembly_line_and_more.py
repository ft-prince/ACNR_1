# Generated by Django 5.0.6 on 2024-08-22 12:57

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0015_assemblyline_number_alter_assemblyline_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productionplan",
            name="assembly_line",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="screen_app.assemblyline",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dailyproductionplan",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="productionplan",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

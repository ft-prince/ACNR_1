# Generated by Django 5.1 on 2024-08-26 20:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screen_app", "0021_remove_screen_upload_pdf"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductionPlanTotal",
            fields=[
                ("s_no", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("total_qty_planned", models.IntegerField(default=0)),
                ("total_qty_actual", models.IntegerField(default=0)),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="screen_app.unit",
                    ),
                ),
            ],
            options={
                "verbose_name": "Daily Production Plan Vs Actual Total",
                "verbose_name_plural": "Daily Production Plan Vs Actual Totals",
                "ordering": ["date", "s_no"],
                "unique_together": {("date", "unit")},
            },
        ),
    ]

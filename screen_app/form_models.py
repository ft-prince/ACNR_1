from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Unit


class WeeklyProductionPlan(models.Model):
    start_date = models.DateField()
    # If you need the month separately, you can derive it in methods or use a custom property
    # month = models.CharField(max_length=10)

    def __str__(self):
        return f"Weekly starting {self.start_date}"

    # Optionally, add a property to get the month from start_date if needed
    @property
    def month(self):
        return self.start_date.strftime('%B %Y')  # e.g., 'August 2024'


class DailyPlan(models.Model):
    weekly_plan = models.ForeignKey(WeeklyProductionPlan, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.IntegerField(default=0, blank=True, null=True)  # Allow blank and null for quantity
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Daily plans for weekly production"
  

    def __str__(self):
        return f"{self.date} - {self.unit}"  # Adjusted to use unit name instead of plan_type_display

from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import os
from django.core.files.base import ContentFile
import zipfile


class Product(models.Model): 
    TA_CHOICES = [
        ('TA100-70020', 'TA100-70020'),
        ('TA100-11050', 'TA100-11050'),
        ('TA100-11051', 'TA100-11051'),
        ('TA100-11052', 'TA100-11052'),
        ('TA100-11053', 'TA100-11053'),
        ('TA100-11054', 'TA100-11054'),
        ('TA100-11055', 'TA100-11055'),
        ('TA100-11056', 'TA100-11056'),
        ('TA100-11057', 'TA100-11057'),
        ('TA100-11058', 'TA100-11058'),
    ]
    
    name = models.CharField(
        max_length=15,
        choices=TA_CHOICES,
        default='TA100-70020',
    )
    status_choices = [
        ('RUNNING', 'Running'),
        ('STOPPED', 'Stopped'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='STOPPED')

    def __str__(self):
        return self.name

# -------------------------------
class Unit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.model}"


class UnitMedia(models.Model):
    unit = models.ForeignKey(Unit, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='unit_media/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mov', 'zip'])]
    )
    duration = models.PositiveIntegerField(default=30,blank=True)  # Duration in seconds

    def __str__(self):
        return f"{self.unit.code} - {self.file.name}"



class Station(models.Model):
    name = models.CharField(max_length=100)
    units = models.ManyToManyField(Unit, related_name='stations')
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_media = models.ManyToManyField(UnitMedia, related_name='stations', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('station_detail', kwargs={'pk': self.pk})

class PDFFile(models.Model):
    pdf_duration = models.IntegerField(default=20,help_text="Duration of pdf in seconds")
    pdf_name = models.CharField(max_length=100,default='TA100-70020' ,help_text="Name of PDF file")
    pdf_file = models.FileField(upload_to='static/media/Pdf_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.pdf_name

class Images(models.Model):
    image_name = models.CharField(max_length=100, default='Image_Name', help_text="Name of Image file")
    image_file = models.ImageField(upload_to='static/media/Images/', help_text="Upload PNG or JPG image")
    uploaded_at = models.DateTimeField(default=timezone.now)
    image_duration = models.IntegerField(default=20, help_text="Duration in seconds (positive integer)")
        
    def __str__(self):
        return self.image_name

    class Meta:
        ordering = ['-uploaded_at']  # Order by upload time (latest first)


class VideoFile(models.Model):
    video_duration = models.IntegerField(default=120,help_text="Duration of video in seconds")
    video_name = models.CharField(max_length=100,default='TA100-70020' ,help_text="Name of Media file")
    video_file = models.FileField(upload_to='static/media/Videos_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.video_name

class Screen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    upload_images = models.ManyToManyField(Images, blank=True)
    upload_video = models.ManyToManyField(VideoFile, blank=True)

    def __str__(self):
        return f"Screen {self.screen_id} at {self.manager} "
    


class AssemblyLine(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Assembly Line {self.number}"
    
# Daily Production Plan Vs Actual
class DailyProductionPlan(models.Model):
    s_no = models.AutoField(primary_key=True)
    # date = models.DateField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    assembly_line = models.ForeignKey(AssemblyLine, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField(default=0,blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.unit.model} - {self.assembly_line}"

    class Meta:
        verbose_name = "Daily Production Plan Vs Actual Total"
        verbose_name_plural = "Daily Production Plan Vs Actual Total"
        ordering = ['date', 's_no']



# Daily Production Plan Vs Actual 
class ProductionPlan(models.Model):
    s_no = models.AutoField(primary_key=True)    
    # date = models.DateField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    assembly_line = models.ForeignKey(AssemblyLine, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField(default=0,blank=True)
    remarks = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.date} - {self.unit.model}"
    class Meta:
        verbose_name = "Daily Production Plan Vs Actual LineWise"
        verbose_name_plural = "Daily Production Plan Vs Actual Total LineWise"        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ProductionPlanTotal.update_or_create_total(self.date, self.unit)



# ----------------------------------------------------------------------------------------
# total

class ProductionPlanTotal(models.Model):
    s_no = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    total_qty_planned = models.IntegerField(default=0)
    total_qty_actual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.unit.model} - Total"

    class Meta:
        verbose_name = "Daily Production Plan Vs Actual Total"
        verbose_name_plural = "Daily Production Plan Vs Actual Totals"
        ordering = ['date', 's_no']
        unique_together = ['date', 'unit']

    @classmethod
    def update_or_create_total(cls, date, unit):
        total_qty_planned = ProductionPlan.objects.filter(
            date=date, unit=unit
        ).aggregate(total=models.Sum('qty_planned'))['total'] or 0

        total_qty_actual = ProductionPlan.objects.filter(
            date=date, unit=unit
        ).aggregate(total=models.Sum('qty_actual'))['total'] or 0

        obj, created = cls.objects.update_or_create(
            date=date,
            unit=unit,
            defaults={
                'total_qty_planned': total_qty_planned,
                'total_qty_actual': total_qty_actual,
            }
        )
        return obj


# -------------------------------------------------------


# class RollingWeeklyProductionPlan(models.Model):
#     unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     qty_planned_day_1 = models.IntegerField(blank=True, null=True)  # 25-Jul-24
#     qty_planned_day_2 = models.IntegerField(blank=True, null=True)  # 26-Jul-24
#     qty_planned_day_3 = models.IntegerField(blank=True, null=True)  # 27-Jul-24
#     qty_planned_day_4 = models.IntegerField(blank=True, null=True)  # 29-Jul-24
#     qty_planned_day_5 = models.IntegerField(blank=True, null=True)  # 30-Jul-24
#     qty_planned_day_6 = models.IntegerField(blank=True, null=True)  # 31-Jul-24
#     remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Plan for {self.unit.unit_code} starting {self.start_date}"




# from django.db import models
# from django.utils import timezone

# class WeeklyPlan(models.Model):
#     unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
#     week_start_date = models.DateField()
#     serial_number = models.IntegerField()
#     remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Plan for {self.unit} - Week of {self.week_start_date}"

#     class Meta:
#         unique_together = ['unit', 'week_start_date', 'serial_number']

# class DailyPlan(models.Model):
#     weekly_plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE, related_name='daily_plans')
#     date = models.DateField()
#     field1 = models.IntegerField()
#     field2 = models.IntegerField()
#     field3 = models.IntegerField()
#     field4 = models.IntegerField()
#     field5 = models.IntegerField()
#     field6 = models.IntegerField()

#     def __str__(self):
#         return f"Plan for {self.weekly_plan.unit} on {self.date}"

#     class Meta:
#         unique_together = ['weekly_plan', 'date']

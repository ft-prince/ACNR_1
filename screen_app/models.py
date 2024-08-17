from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload_pdf = models.ManyToManyField(PDFFile, blank=True)
    upload_images = models.ManyToManyField(Images, blank=True)
    upload_video = models.ManyToManyField(VideoFile, blank=True)

    def __str__(self):
        return f"Screen {self.screen_id} at {self.manager} for {self.product}"
    

# -------------------------------
class Unit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.model}"


class AssemblyLine(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Assembly Line {self.number}"
    
# Daily Production Plan Vs Actual
class DailyProductionPlan(models.Model):
    s_no = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    assembly_line = models.ForeignKey(AssemblyLine, on_delete=models.PROTECT)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField()
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
    date = models.DateField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.unit.model}"

    class Meta:
        verbose_name = "Daily Production Plan Vs Actual LineWise"
        verbose_name_plural = "Daily Production Plan Vs Actual Total LineWise"        



from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F
from .models import DailyProductionPlan, AssemblyLine, Unit
from .forms import DailyProductionPlanForm
from django.core.paginator import Paginator

def production_list(request):
    plans = DailyProductionPlan.objects.all().order_by('-date', 'assembly_line', 's_no')
    paginator = Paginator(plans, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'production_list.html', {'page_obj': page_obj})

def production_detail(request, pk):
    plan = get_object_or_404(DailyProductionPlan, pk=pk)
    return render(request, 'production_detail.html', {'plan': plan})

def production_create(request):
    if request.method == 'POST':
        form = DailyProductionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = DailyProductionPlanForm()
    return render(request, 'production_form.html', {'form': form})

def production_update(request, pk):
    plan = get_object_or_404(DailyProductionPlan, pk=pk)
    if request.method == 'POST':
        form = DailyProductionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('production_list')
    else:
        form = DailyProductionPlanForm(instance=plan)
    return render(request, 'production_form.html', {'form': form})

def production_delete(request, pk):
    plan = get_object_or_404(DailyProductionPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('production_list')
    return render(request, 'production_confirm_delete.html', {'plan': plan})

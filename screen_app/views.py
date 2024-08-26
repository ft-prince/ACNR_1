import datetime
import json
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from matplotlib.table import Cell
import openpyxl
from .models import Screen, PDFFile, VideoFile
from .forms import ScreenForm, PDFFileForm, VideoFileForm,ImageForm
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


def home(request):
    return render(request, 'screen_app/home.html')

staff_member_required_cbv = method_decorator(staff_member_required, name='dispatch')

# Screen views
@staff_member_required_cbv
class ScreenListView(ListView):
    model = Screen
    template_name = 'CRUD/screen_list.html'
    context_object_name = 'screens'

# @staff_member_required_cbv
class ScreenDetailView(DetailView):
    model = Screen
    template_name = 'CRUD/screen_detail.html'

@staff_member_required_cbv
class ScreenCreateView(CreateView):
    model = Screen
    form_class = ScreenForm
    template_name = 'CRUD/screen_form.html'
    success_url = reverse_lazy('screen_list')

@staff_member_required_cbv
class ScreenUpdateView(UpdateView):
    model = Screen
    form_class = ScreenForm
    template_name = 'CRUD/screen_form.html'
    success_url = reverse_lazy('screen_list')

@staff_member_required_cbv
class ScreenDeleteView(DeleteView):
    model = Screen
    template_name = 'CRUD/screen_confirm_delete.html'
    success_url = reverse_lazy('screen_list')

@staff_member_required
def add_content_to_screen(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    
    if request.method == 'POST':
        pdf_form = PDFFileForm(request.POST, request.FILES, prefix='pdf')
        video_form = VideoFileForm(request.POST, request.FILES, prefix='video')
        image_form = ImageForm(request.POST, request.FILES, prefix='image')
        
        if 'pdf_submit' in request.POST and pdf_form.is_valid():
            pdf = pdf_form.save()
            screen.upload_pdf.add(pdf)
            return redirect('screen_detail', pk=screen_id)
        
        if 'video_submit' in request.POST and video_form.is_valid():
            video = video_form.save()
            screen.upload_video.add(video)
            return redirect('screen_detail', pk=screen_id)
        # Handle Image form submission
        if 'image_submit' in request.POST and image_form.is_valid():
            image = image_form.save()
            screen.upload_images.add(image)
            return redirect('screen_detail', pk=screen_id)
        
    else:
        pdf_form = PDFFileForm(prefix='pdf')
        video_form = VideoFileForm(prefix='video')
        image_form = ImageForm(prefix='image')
    
    return render(request, 'CRUD/add_content_to_screen.html', {
        'screen': screen,
        'pdf_form': pdf_form,
        'video_form': video_form,
        'image_form': image_form,  # Pass the ImageForm to the template
        
    })

# PDF Views
@staff_member_required_cbv
class PDFFileListView(ListView):
    model = PDFFile
    template_name = 'pdfs/pdf_list.html'
    context_object_name = 'pdfs'

@staff_member_required_cbv
class PDFFileDetailView(DetailView):
    model = PDFFile
    template_name = 'pdfs/pdf_detail.html'

@staff_member_required_cbv
class PDFFileCreateView(CreateView):
    model = PDFFile
    form_class = PDFFileForm
    template_name = 'pdfs/pdf_form.html'
    success_url = reverse_lazy('pdf_list')

@staff_member_required_cbv
class PDFFileUpdateView(UpdateView):
    model = PDFFile
    form_class = PDFFileForm
    template_name = 'pdfs/pdf_form.html'
    success_url = reverse_lazy('pdf_list')

@staff_member_required_cbv
class PDFFileDeleteView(DeleteView):
    model = PDFFile
    template_name = 'pdfs/pdf_confirm_delete.html'
    success_url = reverse_lazy('pdf_list')

# Video Views
@staff_member_required_cbv
class VideoFileListView(ListView):
    model = VideoFile
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 10  # Number of items per page

@staff_member_required_cbv
class VideoFileDetailView(DetailView):
    model = VideoFile
    template_name = 'videos/video_detail.html'

@staff_member_required_cbv
class VideoFileCreateView(CreateView):
    model = VideoFile
    form_class = VideoFileForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('video_list')

@staff_member_required_cbv
class VideoFileUpdateView(UpdateView):
    model = VideoFile
    form_class = VideoFileForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('video_list')

@staff_member_required_cbv
class VideoFileDeleteView(DeleteView):
    model = VideoFile
    template_name = 'videos/video_confirm_delete.html'
    success_url = reverse_lazy('video_list')


#  sliders

def screen_slider(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    videos = screen.upload_video.all()
    context = {
        'screen': screen,
        'videos': videos,
    }
    return render(request, 'screen_app/screen_slider.html', context)


def pdf_slider(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    pdfs = screen.upload_pdf.all()
    context = {
        'screen': screen,
        'pdfs': pdfs,
    }
    return render(request, 'screen_app/pdf_slider.html', context)


def slideshow_view(request, screen_id):
    # Fetch the screen object based on screen_id
    screen = get_object_or_404(Screen, screen_id=screen_id)
    
    # Assuming 'upload_video' is the ManyToManyField related name for videos in 'addMultipleFiles'
    media_files = screen.upload_video.all()

    context = {
        'media_files': media_files,
        'screen_id': screen_id
    }
    return render(request, 'slideshow/screen_slider.html', context)



def pdf_slideshow_view(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    pdf_files = screen.upload_pdf.all()

    return render(request, 'slideshow/pdf_slideshow.html', {
        'pdf_files': pdf_files,
            'screen_id': screen_id

    })

# ----------------------------------------------------------------
from django.shortcuts import render
from .models import ProductionPlan, DailyProductionPlan

def production_plan_list(request):
    plans = ProductionPlan.objects.all()
    return render(request, 'Production/production_plan_list.html', {'plans': plans})

def production_plan_list2(request):
    plans = DailyProductionPlan.objects.all()
    return render(request, 'Production/DailyProductionPlan_list.html', {'plans': plans})

# ---------------------------------------------------------------


from .models import Images

def display_images(request):
    images = Images.objects.all()
    context = {
        'images': images,
    }
    return render(request, 'display_images.html', context)


from django.shortcuts import render
from .models import Images
from .serializers import ImageSerializer

# def slider_view(request):
#     images = Images.objects.all().order_by('-uploaded_at')  # Get latest images
#     serializer = ImageSerializer(images, many=True)
#     context = {'images': serializer.data}
#     return render(request, 'slider2.html', context)


def image_slider_view(request):
    images = Images.objects.all()
    return render(request, 'slider2.html', {'images': images})

# --------------------------------------------

from django.shortcuts import render
from .models import Screen

def screen_slider(request, screen_id):
    screen = Screen.objects.get(screen_id=screen_id)

    # Combine images and videos in a single list
    media_files = []

    for image in screen.upload_images.all():
        media_files.append({
            'type': 'image',
            'file_url': image.image_file.url,
            'name': image.image_name,
            'duration': image.image_duration
        })

    for video in screen.upload_video.all():
        media_files.append({
            'type': 'video',
            'file_url': video.video_file.url,
            'name': video.video_name,
            'duration': video.video_duration
        })

    context = {
        'media_files': media_files,
    }
    return render(request, 'screen_slider.html', context)


# -----------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import DailyProductionPlan, Unit, AssemblyLine
from .forms import DailyProductionPlanForm
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.generic import ListView
from .models import DailyProductionPlan, AssemblyLine

class DailyProductionPlanListView(ListView):
    model = DailyProductionPlan
    template_name = 'daily/production_plan_list.html'
    context_object_name = 'plans'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date')

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                date = datetime.today().date()
        else:
            date = datetime.today().date()

        queryset = queryset.filter(date=date)

        assembly_line = self.request.GET.get('assembly_line')
        if assembly_line:
            queryset = queryset.filter(assembly_line__name=assembly_line)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assembly_lines = AssemblyLine.objects.all()
        context['assembly_lines'] = assembly_lines

        date_str = self.request.GET.get('date')
        if date_str:
            try:
                current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                current_date = datetime.today().date()
        else:
            current_date = datetime.today().date()

        previous_date = current_date - timedelta(days=1)
        next_date = current_date + timedelta(days=1)

        context['current_date'] = current_date.strftime("%Y-%m-%d")
        context['previous_date'] = previous_date.strftime("%Y-%m-%d")
        context['next_date'] = next_date.strftime("%Y-%m-%d")

        return context


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DailyProductionPlan
import json

@csrf_exempt
def update_daily_actual_value_total(request, plan_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qty_actual = data.get('qty_actual')

            # Validate input
            if qty_actual is None:
                return JsonResponse({'success': False, 'error': 'No quantity provided'}, status=400)
            
            # Ensure qty_actual is a valid integer
            try:
                qty_actual = int(qty_actual)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Quantity must be an integer'}, status=400)

            # Update the plan
            plan = DailyProductionPlan.objects.get(s_no=plan_id)
            plan.qty_actual = qty_actual
            plan.save()

            return JsonResponse({'success': True})
        except DailyProductionPlan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Plan not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # Log the exception for further inspection
            import logging
            logger = logging.getLogger(__name__)
            logger.error('Unexpected error: %s', str(e), exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


class DailyProductionPlanDetailView(DetailView):
    model = DailyProductionPlan
    template_name = 'daily/production_plan_detail.html'
    context_object_name = 'plan'

from django.shortcuts import render, redirect
from .models import AssemblyLine, Unit, ProductionPlan
from datetime import datetime
from django.utils import timezone

def add_production_plan(request):
    if request.method == 'POST':
        form = DailyProductionPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.date = form.cleaned_data['date']
            plan.save()
            return redirect('production_plan_list')
    else:
        form = DailyProductionPlanForm()

    # Fetch assembly lines to populate the dropdown
    assembly_lines = AssemblyLine.objects.all()
    units = Unit.objects.all()  # Assuming you also need units

    return render(request, 'daily/add_production_plan.html', {
        'form': form,
        'assembly_lines': assembly_lines,
        'units': units,
        'today_date': datetime.today().date().strftime("%Y-%m-%d"),
    })


def search_units(request):
    query = request.GET.get('query', '')
    units = Unit.objects.filter(
        Q(code__icontains=query) | Q(model__icontains=query)
    )[:10]  # Limit to 10 results
    data = [{'id': unit.id, 'text': f"{unit.code} - {unit.model}"} for unit in units]
    return JsonResponse({'results': data})


# --------------------------------------------
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Sum
from .models import DailyProductionPlan, AssemblyLine

def assembly_line_production(request, assembly_line_number):
    assembly_line = get_object_or_404(AssemblyLine, number=assembly_line_number)
    
    # Use today's date if none is provided
    date_str = request.GET.get('date', None)
    if date_str is None or date_str == 'today':
        date = datetime.today().date()
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Format the date as "day-month-year"
    formatted_date = date.strftime("%d-%m-%Y")

    plans = DailyProductionPlan.objects.filter(
        date=date,
        assembly_line=assembly_line
    ).order_by('s_no')

    total_planned = plans.aggregate(Sum('qty_planned'))['qty_planned__sum'] or 0
    total_actual = plans.aggregate(Sum('qty_actual'))['qty_actual__sum'] or 0

    for plan in plans:
        plan.difference = plan.qty_planned - plan.qty_actual
        if plan.qty_actual == 0:
            plan.status = "Pending"
        elif plan.qty_actual < plan.qty_planned:
            plan.status = "In-Prog."
        elif plan.qty_actual >= plan.qty_planned:
            plan.status = "Completed"
        else:
            plan.status = plan.remarks  # Fallback for any unexpected scenarios

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'assembly_line': assembly_line.name,
            'current_date': formatted_date,  # Pass the formatted date here
            'plans': list(plans.values('s_no', 'unit__code', 'unit__model', 'qty_planned', 'qty_actual', 'status')),
            'total_planned': total_planned,
            'total_actual': total_actual,
        }
        return JsonResponse(data)

    context = {
        'assembly_line': assembly_line,
        'current_date': formatted_date,  # Pass the formatted date here
        'plans': plans,
        'total_planned': total_planned,
        'total_actual': total_actual,
    }
    return render(request, 'daily/assembly_line_production.html', context)


# ----------------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import ProductionPlan, Unit, AssemblyLine
from .forms import ProductionPlanForm
from django.http import JsonResponse



from django.views.generic import ListView
from .models import ProductionPlan, AssemblyLine

    
from datetime import datetime, timedelta

from django.views.generic import ListView
from datetime import datetime, timedelta

class ProductionPlanListView(ListView):
    model = ProductionPlan
    template_name = 'linewise/production_plan_list.html'
    context_object_name = 'plans'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date')

        if date:
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                date = datetime.today().date()
        else:
            date = datetime.today().date()

        queryset = queryset.filter(date=date)

        assembly_line = self.request.GET.get('assembly_line')
        if assembly_line:
            queryset = queryset.filter(assembly_line__name=assembly_line)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assembly_lines = AssemblyLine.objects.all()
        context['assembly_lines'] = assembly_lines

        date_str = self.request.GET.get('date')
        if date_str:
            try:
                current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                current_date = datetime.today().date()
        else:
            current_date = datetime.today().date()

        previous_date = current_date - timedelta(days=1)
        next_date = current_date + timedelta(days=1)

        context['current_date'] = current_date.strftime("%Y-%m-%d")
        context['previous_date'] = previous_date.strftime("%Y-%m-%d")
        context['next_date'] = next_date.strftime("%Y-%m-%d")

        return context


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProductionPlan

@csrf_exempt
def update_actual_value(request, plan_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qty_actual = data.get('qty_actual')
            
            # Validate input
            if not qty_actual:
                return JsonResponse({'success': False, 'error': 'No quantity provided'}, status=400)
            
            plan = ProductionPlan.objects.get(s_no=plan_id)
            plan.qty_actual = qty_actual
            plan.save()

            return JsonResponse({'success': True})
        except ProductionPlan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Plan not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


from django.http import JsonResponse

def update_actual_view(request, pk):
    if request.method == 'POST':
        try:
            plan = ProductionPlan.objects.get(pk=pk)
            data = json.loads(request.body)
            plan.qty_actual = data.get('qty_actual')
            plan.save()
            return JsonResponse({'success': True})
        except ProductionPlan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Plan not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

        
class ProductionPlanDetailView(DetailView):
    model = ProductionPlan
    template_name = 'linewise/production_plan_detail.html'
    context_object_name = 'plan'

def add_production_plan_linewise(request):
    if request.method == 'POST':
        form = ProductionPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.date = form.cleaned_data['date']
            plan.save()
            return redirect('production_plan_list_linewise')
    else:
        form = ProductionPlanForm()

    # Fetch assembly lines to populate the dropdown
    assembly_lines = AssemblyLine.objects.all()
    units = Unit.objects.all()  # Assuming you also need units

    return render(request, 'linewise/add_production_plan.html', {
        'form': form,
        'assembly_lines': assembly_lines,
        'units': units,
        'today_date': datetime.today().date().strftime("%Y-%m-%d"),
    })


def search_units_linewise(request):
    query = request.GET.get('query', '')
    units = Unit.objects.filter(
        Q(code__icontains=query) | Q(model__icontains=query)
    )[:10]  # Limit to 10 results
    data = [{'id': unit.id, 'text': f"{unit.code} - {unit.model}"} for unit in units]
    return JsonResponse({'results': data})


# --------------------------------------------
# from django.shortcuts import render, get_object_or_404
# from django.db.models import Sum

# def assembly_line_production_linewise(request, assembly_line_number, date):
#     assembly_line = get_object_or_404(AssemblyLine, number=assembly_line_number)
#     plans = ProductionPlan.objects.filter(
#         date=date,
#         assembly_line=assembly_line
#     ).order_by('s_no')
    
#     total_planned = plans.aggregate(Sum('qty_planned'))['qty_planned__sum'] or 0
#     total_actual = plans.aggregate(Sum('qty_actual'))['qty_actual__sum'] or 0
    
#     for plan in plans:
#         plan.difference = plan.qty_planned - plan.qty_actual
#         if plan.qty_actual == 0:
#             plan.status = "Pending"
#         elif plan.qty_actual < plan.qty_planned:
#             plan.status = "In Progress"
#         elif plan.qty_actual >= plan.qty_planned:
#             plan.status = "Completed"
#         else:
#             plan.status = plan.remarks  # Fallback for any unexpected scenarios
    
#     context = {
#         'assembly_line': assembly_line,
#         'current_date': date,
#         'plans': plans,
#         'total_planned': total_planned,
#         'total_actual': total_actual,
#     }
#     return render(request, 'linewise/assembly_line_production.html', context)


from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Sum
from .models import ProductionPlan, AssemblyLine

def assembly_line_production_linewise(request, assembly_line_number):
    assembly_line = get_object_or_404(AssemblyLine, number=assembly_line_number)
    
    # Use today's date if none is provided
    date_str = request.GET.get('date', None)
    if date_str is None or date_str == 'today':
        date = datetime.today().date()
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Format the date as "day-month-year"
    formatted_date = date.strftime("%d-%m-%Y")
    
    plans = ProductionPlan.objects.filter(
        date=date,
        assembly_line=assembly_line
    ).order_by('s_no')

    total_planned = plans.aggregate(Sum('qty_planned'))['qty_planned__sum'] or 0
    total_actual = plans.aggregate(Sum('qty_actual'))['qty_actual__sum'] or 0

    for plan in plans:
        plan.difference = plan.qty_planned - plan.qty_actual
        if plan.qty_actual == 0:
            plan.status = "Pending"
        elif plan.qty_actual < plan.qty_planned:
            plan.status = "In-Prog."
        elif plan.qty_actual >= plan.qty_planned:
            plan.status = "Completed"
        else:
            plan.status = plan.remarks  # Fallback for any unexpected scenarios

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'assembly_line': assembly_line.name,
            'current_date': formatted_date,  # Pass the formatted date here
            'plans': list(plans.values('s_no', 'unit__code', 'unit__model', 'qty_planned', 'qty_actual', 'status')),
            'total_planned': total_planned,
            'total_actual': total_actual,
        }
        return JsonResponse(data)

    context = {
        'assembly_line': assembly_line,
        'current_date': formatted_date,  # Pass the formatted date here
        'plans': plans,
        'total_planned': total_planned,
        'total_actual': total_actual,
    }
    return render(request, 'linewise/assembly_line_production.html', context)



# ----------------------------------------------------------------
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import ProductionPlan
from datetime import datetime

def export_production_plan_pdf(request):
    # Apply the same filtering logic as in ProductionPlanListView
    queryset = ProductionPlan.objects.all()
    date = request.GET.get('date')

    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            date = datetime.today().date()
    else:
        date = datetime.today().date()

    queryset = queryset.filter(date=date)

    assembly_line = request.GET.get('assembly_line')
    if assembly_line:
        queryset = queryset.filter(assembly_line__name=assembly_line)

    # Create the HttpResponse object with PDF headers
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph(f"Daily Production Plan - {date}", styles['Title'])
    elements.append(title)

    # Create table data
    data = [['Date', 'Unit Code', 'Unit Model', 'Assembly Line', 'Planned Qty', 'Actual Qty']]
    for plan in queryset:
        data.append([
            plan.date.strftime("%Y-%m-%d"),
            plan.unit.code,
            plan.unit.model,
            plan.assembly_line.name,
            str(plan.qty_planned),
            str(plan.qty_actual)
        ])

    # Create table
    table = Table(data)

    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add table to elements
    elements.append(table)

    # Build PDF
    doc.build(elements)
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

import pandas as pd
from django.http import HttpResponse
from .models import ProductionPlan
from datetime import datetime
from io import BytesIO

def export_production_plan_to_excel(request):
    # Apply the same filtering logic as in ProductionPlanListView
    queryset = ProductionPlan.objects.all()
    date = request.GET.get('date')

    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            date = datetime.today().date()
    else:
        date = datetime.today().date()

    queryset = queryset.filter(date=date)

    assembly_line = request.GET.get('assembly_line')
    if assembly_line:
        queryset = queryset.filter(assembly_line__name=assembly_line)

    # Convert to DataFrame
    data = list(queryset.values('date', 'unit__code', 'unit__model', 'assembly_line__name', 'qty_planned', 'qty_actual'))
    df = pd.DataFrame(data)

    # Rename columns for better readability
    df.columns = ['Date', 'Unit Code', 'Unit Model', 'Assembly Line', 'Planned Qty', 'Actual Qty']

    # Create a Pandas Excel writer using XlsxWriter as the engine
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write the dataframe to the worksheet
        df.to_excel(writer, sheet_name='Production Plans', index=False, startrow=1)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Production Plans']

        # Add a title
        title = f"Daily Production Plan - {date}"
        worksheet.write(0, 0, title, workbook.add_format({'bold': True, 'font_size': 16}))

        # Get the dimensions of the dataframe
        (max_row, max_col) = df.shape

        # Create a format for the header row
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })

        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(1, col_num, value, header_format)

        # Set the column width and format
        worksheet.set_column(0, 0, 15)  # Date
        worksheet.set_column(1, 1, 15)  # Unit Code
        worksheet.set_column(2, 2, 20)  # Unit Model
        worksheet.set_column(3, 3, 20)  # Assembly Line
        worksheet.set_column(4, 4, 15)  # Planned Qty
        worksheet.set_column(5, 5, 15)  # Actual Qty

        # Add borders to all cells
        border_fmt = workbook.add_format({'border': 1})
        worksheet.conditional_format(1, 0, max_row+1, max_col-1, {'type': 'no_errors', 'format': border_fmt})

    # Create the HttpResponse object with Excel content
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="production_plan_{date}.xlsx"'

    return response



# --------------------------------------------------------------------------------------------------------------------------------
#   FOR TOTALS ONLY FOR
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import DailyProductionPlan
from datetime import datetime

def export_production_plan_total_pdf(request):
    # Apply the same filtering logic as in DailyProductionPlanListView
    queryset = DailyProductionPlan.objects.all()
    date = request.GET.get('date')

    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            date = datetime.today().date()
    else:
        date = datetime.today().date()

    queryset = queryset.filter(date=date)

    assembly_line = request.GET.get('assembly_line')
    if assembly_line:
        queryset = queryset.filter(assembly_line__name=assembly_line)

    # Create the HttpResponse object with PDF headers
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph(f"Daily Production Plan for Total - {date}", styles['Title'])
    elements.append(title)

    # Create table data
    data = [['Date', 'Unit Code', 'Unit Model', 'Assembly Line', 'Planned Qty', 'Actual Qty']]
    for plan in queryset:
        data.append([
            plan.date.strftime("%Y-%m-%d"),
            plan.unit.code,
            plan.unit.model,
            plan.assembly_line.name,
            str(plan.qty_planned),
            str(plan.qty_actual)
        ])

    # Create table
    table = Table(data)

    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add table to elements
    elements.append(table)

    # Build PDF
    doc.build(elements)
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

import pandas as pd
from django.http import HttpResponse
from .models import DailyProductionPlan
from datetime import datetime
from io import BytesIO

def export_production_plan_total_to_excel(request):
    # Apply the same filtering logic as in DailyProductionPlanListView
    queryset = DailyProductionPlan.objects.all()
    date = request.GET.get('date')

    if date:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            date = datetime.today().date()
    else:
        date = datetime.today().date()

    queryset = queryset.filter(date=date)

    assembly_line = request.GET.get('assembly_line')
    if assembly_line:
        queryset = queryset.filter(assembly_line__name=assembly_line)

    # Convert to DataFrame
    data = list(queryset.values('date', 'unit__code', 'unit__model', 'assembly_line__name', 'qty_planned', 'qty_actual'))
    df = pd.DataFrame(data)

    # Rename columns for better readability
    df.columns = ['Date', 'Unit Code', 'Unit Model', 'Assembly Line', 'Planned Qty', 'Actual Qty']

    # Create a Pandas Excel writer using XlsxWriter as the engine
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write the dataframe to the worksheet
        df.to_excel(writer, sheet_name='Production Plans', index=False, startrow=1)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Production Plans']

        # Add a title
        title = f"Daily Production Plan Total - {date} "
        worksheet.write(0, 0, title, workbook.add_format({'bold': True, 'font_size': 16}))

        # Get the dimensions of the dataframe
        (max_row, max_col) = df.shape

        # Create a format for the header row
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })

        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(1, col_num, value, header_format)

        # Set the column width and format
        worksheet.set_column(0, 0, 15)  # Date
        worksheet.set_column(1, 1, 15)  # Unit Code
        worksheet.set_column(2, 2, 20)  # Unit Model
        worksheet.set_column(3, 3, 20)  # Assembly Line
        worksheet.set_column(4, 4, 15)  # Planned Qty
        worksheet.set_column(5, 5, 15)  # Actual Qty

        # Add borders to all cells
        border_fmt = workbook.add_format({'border': 1})
        worksheet.conditional_format(1, 0, max_row+1, max_col-1, {'type': 'no_errors', 'format': border_fmt})

    # Create the HttpResponse object with Excel content
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="production_plan_total_{date}.xlsx"'

    return response




# ----------------------------------------------------------------


from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum
from .form_models import WeeklyProductionPlan, DailyPlan, Unit
from .forms import WeeklyProductionPlanForm, DailyPlanForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import pandas as pd

class WeeklyProductionPlanListView(ListView):
    model = WeeklyProductionPlan
    template_name = 'weekly/production_plan_list.html'
    context_object_name = 'plans'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        month = self.request.GET.get('month')

        if month:
            try:
                month_date = datetime.strptime(month, "%Y-%m")
                queryset = queryset.filter(start_date__year=month_date.year, start_date__month=month_date.month)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month'] = self.request.GET.get('month', datetime.now().strftime("%Y-%m"))
        return context

class WeeklyProductionPlanDetailView(DetailView):
    model = WeeklyProductionPlan
    template_name = 'weekly/production_plan_detail.html'
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['daily_plans'] = self.object.dailyplan_set.all().order_by('date')  # This fetches related DailyPlan objects
        return context

@csrf_exempt
def update_weekly_daily_plan(request, plan_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            
            if quantity is None:
                return JsonResponse({'success': False, 'error': 'No quantity provided'}, status=400)
            
            daily_plan = DailyPlan.objects.get(id=plan_id)
            daily_plan.quantity = quantity
            daily_plan.save()

            return JsonResponse({'success': True})
        except DailyPlan.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Plan not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

def add_weekly_production_plan(request):
    if request.method == 'POST':
        form = WeeklyProductionPlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            return redirect('weekly_production_plan_list')
    else:
        form = WeeklyProductionPlanForm()

    return render(request, 'weekly/add_production_plan.html', {
        'form': form,
    })

def add_weekly_daily_plan(request):
    if request.method == 'POST':
        form = DailyPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()
            return redirect('weekly_production_plan_detail', pk=plan.weekly_plan.id)
    else:
        form = DailyPlanForm()

    units = Unit.objects.all()
    weekly_plans = WeeklyProductionPlan.objects.all()

    return render(request, 'weekly/add_daily_plan.html', {
        'form': form,
        'units': units,
        'weekly_plans': weekly_plans,
    })

def search_weekly_units(request):
    query = request.GET.get('query', '')
    units = Unit.objects.filter(
        Q(code__icontains=query) | Q(model__icontains=query)
    )[:10]  # Limit to 10 results
    data = [{'id': unit.id, 'text': f"{unit.code} - {unit.model}"} for unit in units]
    return JsonResponse({'results': data})

def weekly_production_summary(request, week_id):
    week = get_object_or_404(WeeklyProductionPlan, id=week_id)
    daily_plans = DailyPlan.objects.filter(weekly_plan=week).order_by('date')

    total_quantity = daily_plans.aggregate(Sum('quantity'))['quantity__sum'] or 0

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'week_start': week.start_date.strftime("%Y-%m-%d"),
            'daily_plans': list(daily_plans.values('date', 'unit__code', 'quantity')),
            'total_quantity': total_quantity,
        }
        return JsonResponse(data)

    context = {
        'week': week,
        'daily_plans': daily_plans,
        'total_quantity': total_quantity,
    }
    return render(request, 'weekly/production_summary.html', context)

def export_weekly_plan_pdf(request, week_id):
    week = get_object_or_404(WeeklyProductionPlan, id=week_id)
    daily_plans = DailyPlan.objects.filter(weekly_plan=week).order_by('date')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph(f"Weekly Production Plan - {week.start_date}", styles['Title'])
    elements.append(title)

    data = [['Date', 'Unit Code', 'Unit Model', 'Quantity']]
    for plan in daily_plans:
        data.append([
            plan.date.strftime("%Y-%m-%d"),
            plan.unit.code,
            plan.unit.model,
            str(plan.quantity)
        ])

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)

    doc.build(elements)
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def export_weekly_plan_to_excel(request, week_id):
    week = get_object_or_404(WeeklyProductionPlan, id=week_id)
    daily_plans = DailyPlan.objects.filter(weekly_plan=week).order_by('date')

    data = list(daily_plans.values('date', 'unit__code', 'unit__model', 'quantity'))
    df = pd.DataFrame(data)

    df.columns = ['Date', 'Unit Code', 'Unit Model', 'Quantity']

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Weekly Plan', index=False, startrow=1)

        workbook = writer.book
        worksheet = writer.sheets['Weekly Plan']

        title = f"Weekly Production Plan - {week.start_date}"
        worksheet.write(0, 0, title, workbook.add_format({'bold': True, 'font_size': 16}))

        (max_row, max_col) = df.shape

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(1, col_num, value, header_format)

        worksheet.set_column(0, 0, 15)  # Date
        worksheet.set_column(1, 1, 15)  # Unit Code
        worksheet.set_column(2, 2, 20)  # Unit Model
        worksheet.set_column(3, 3, 15)  # Quantity

        border_fmt = workbook.add_format({'border': 1})
        worksheet.conditional_format(1, 0, max_row+1, max_col-1, {'type': 'no_errors', 'format': border_fmt})

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="weekly_production_plan_{week.start_date}.xlsx"'

    return response




from django.shortcuts import render
from django.views.generic import ListView
from django.utils.timezone import now
from .form_models import WeeklyProductionPlan
from datetime import timedelta

class WeeklyProductionPlansView(ListView):
    model = WeeklyProductionPlan
    template_name = 'weekly/weekly_production_plans.html'

    def get_queryset(self):
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        return WeeklyProductionPlan.objects.filter(date__range=[start_of_week, end_of_week])

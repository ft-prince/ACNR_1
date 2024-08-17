from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Screen, PDFFile, VideoFile
from .forms import ScreenForm, PDFFileForm, VideoFileForm
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
        
        if 'pdf_submit' in request.POST and pdf_form.is_valid():
            pdf = pdf_form.save()
            screen.upload_pdf.add(pdf)
            return redirect('screen_detail', pk=screen_id)
        
        if 'video_submit' in request.POST and video_form.is_valid():
            video = video_form.save()
            screen.upload_video.add(video)
            return redirect('screen_detail', pk=screen_id)
    else:
        pdf_form = PDFFileForm(prefix='pdf')
        video_form = VideoFileForm(prefix='video')
    
    return render(request, 'CRUD/add_content_to_screen.html', {
        'screen': screen,
        'pdf_form': pdf_form,
        'video_form': video_form
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

class DailyProductionPlanListView(ListView):
    model = DailyProductionPlan
    template_name = 'production_plan_list.html'
    context_object_name = 'plans'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date')
        assembly_line = self.request.GET.get('assembly_line')
        
        if date:
            queryset = queryset.filter(date=date)
        if assembly_line:
            queryset = queryset.filter(assembly_line__name=assembly_line)
        
        return queryset

class DailyProductionPlanDetailView(DetailView):
    model = DailyProductionPlan
    template_name = 'production_plan_detail.html'
    context_object_name = 'plan'

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
    
    return render(request, 'add_production_plan.html', {'form': form})


def search_units(request):
    query = request.GET.get('query', '')
    units = Unit.objects.filter(
        Q(code__icontains=query) | Q(model__icontains=query)
    )[:10]  # Limit to 10 results
    data = [{'id': unit.id, 'text': f"{unit.code} - {unit.model}"} for unit in units]
    return JsonResponse({'results': data})


# --------------------------------------------
from django.shortcuts import render, get_object_or_404
from .models import DailyProductionPlan, AssemblyLine
from django.db.models import Sum

def assembly_line_production(request, assembly_line_number, date):
    assembly_line = get_object_or_404(AssemblyLine, number=assembly_line_number)
    plans = DailyProductionPlan.objects.filter(
        date=date,
        assembly_line=assembly_line
    ).order_by('s_no')
    
    total_planned = plans.aggregate(Sum('qty_planned'))['qty_planned__sum'] or 0
    total_actual = plans.aggregate(Sum('qty_actual'))['qty_actual__sum'] or 0
    
    context = {
        'assembly_line': assembly_line,
        'current_date': date,
        'plans': plans,
        'total_planned': total_planned,
        'total_actual': total_actual,
    }
    return render(request, 'assembly_line_production.html', context)



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

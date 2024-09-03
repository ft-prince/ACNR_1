from django.contrib import admin 
from django.utils.html import format_html
from django import forms
from django.urls import path
from .models import PDFFile,VideoFile,Unit, DailyProductionPlan ,ProductionPlan ,AssemblyLine,ProductionPlanTotal,UnitMedia,Station
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import zipfile
from .models import Unit, UnitMedia, Station

# Register your models here.
from .models import Images
from .form_models import WeeklyProductionPlan,DailyPlan
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'uploaded_at')
    search_fields = ('image_name',)
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

# admin.site.register(Images, ImagesAdmin)
# admin.site.register(WeeklyProductionPlan)
# admin.site.register(DailyPlan)
admin.site.register(ProductionPlanTotal)

class UnitMediaInline(admin.TabularInline):
    model = UnitMedia
    extra = 1
    fields = ['file', 'file_preview']
    readonly_fields = ['file_preview']
    def file_preview(self, obj):
        if obj.file:
            file_url = obj.file.url
            file_name = obj.file.name.lower()
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', file_url)
            elif file_name.endswith(('.mp4', '.mov', '.avi')):
                return format_html('<video width="100" height="100" controls><source src="{}" type="video/mp4"></video>', file_url)
            elif file_name.endswith('.zip'):
                return "Zip file (will be processed)"
            else:
                return format_html('<a href="{}">View File</a>', file_url)
        return "No file"

class UnitAdminForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'model']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    form = UnitAdminForm
    list_display = ('code', 'model')
    inlines = [UnitMediaInline]

    def station_list(self, obj):
        return ", ".join([station.name for station in obj.stations.all()])
    station_list.short_description = 'Stations'

@admin.register(UnitMedia)
class UnitMediaAdmin(admin.ModelAdmin):
    list_display = ['unit', 'file', 'file_preview']
    list_filter = ['unit']
    search_fields = ['unit__code', 'unit__model', 'file']
    readonly_fields = ['file_preview']

    def file_preview(self, obj):
        if obj.file:
            file_url = obj.file.url
            file_name = obj.file.name.lower()
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', file_url)
            elif file_name.endswith(('.mp4', '.mov', '.avi')):
                return format_html('<video width="100" height="100" controls><source src="{}" type="video/mp4"></video>', file_url)
            elif file_name.endswith('.zip'):
                return "Zip file (will be processed)"
            else:
                return format_html('<a href="{}">View File</a>', file_url)
        return "No file"
    file_preview.short_description = 'File Preview'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if obj.file and obj.file.name.lower().endswith('.zip'):
            with zipfile.ZipFile(obj.file.path, 'r') as z:
                for filename in z.namelist():
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov')):
                        file_data = z.read(filename)
                        file_name = os.path.basename(filename)
                        content_file = ContentFile(file_data)
                        new_media = UnitMedia(unit=obj.unit)
                        new_media.file.save(file_name, content_file)
            
            # Delete the original zip file after processing
            obj.file.delete()
            obj.delete()
            
            self.message_user(request, 'Zip file contents uploaded successfully!')



class StationAdminForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'units', 'manager', 'selected_media']
        widgets = {
            'selected_media': forms.CheckboxSelectMultiple,  # Allow selecting multiple media files
        }

    def __init__(self, *args, **kwargs):
        super(StationAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # If the station instance exists, filter selected_media by units linked to this station
            self.fields['selected_media'].queryset = UnitMedia.objects.filter(unit__in=self.instance.units.all())
        else:
            # If no station instance, show no media files initially
            self.fields['selected_media'].queryset = UnitMedia.objects.none()

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    form = StationAdminForm
    list_display = ('name', 'manager', 'unit_count', 'image_count')
    filter_horizontal = ('units', 'selected_media')  # Allow selecting multiple units and media

    def unit_count(self, obj):
        return obj.units.count()
    unit_count.short_description = 'Number of Units'

    def image_count(self, obj):
        return obj.selected_media.count()
    image_count.short_description = 'Number of Selected Images'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('unit_count', 'image_count')
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        station = self.get_object(request, object_id)
        if station:
            # Display all media associated with the units linked to this station
            unit_media = UnitMedia.objects.filter(unit__in=station.units.all())
            extra_context['unit_media'] = unit_media
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

# admin.site.register(Station, StationAdmin)


# @admin.register(DailyProductionPlan)
# class DailyProductionPlanAdmin(admin.ModelAdmin):
#     list_display = ('date', 's_no', 'get_unit_code', 'get_unit_model', 'qty_planned', 'qty_actual')

#     def get_unit_code(self, obj):
#         return obj.unit.code
#     get_unit_code.short_description = 'Unit Code'

#     def get_unit_model(self, obj):
#         return obj.unit.model
#     get_unit_model.short_description = 'Unit Model'

@admin.register(AssemblyLine)
class AssemblyLineAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProductionPlan)
class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 's_no', 'get_unit_code', 'get_unit_model', 'qty_planned', 'qty_actual')

    def get_unit_code(self, obj):
        return obj.unit.code
    get_unit_code.short_description = 'Unit Code'

    def get_unit_model(self, obj):
        return obj.unit.model
    get_unit_model.short_description = 'Unit Model'

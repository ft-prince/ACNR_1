from django.contrib import admin 

from .models import Product, Screen ,PDFFile,VideoFile,Unit, DailyProductionPlan ,ProductionPlan ,AssemblyLine,ProductionPlanTotal

# Register your models here.
admin.site.register(Product)
admin.site.register(Screen)
admin.site.register(VideoFile)
admin.site.register(PDFFile)
from .models import Images
from .form_models import WeeklyProductionPlan,DailyPlan
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'uploaded_at')
    search_fields = ('image_name',)
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

admin.site.register(Images, ImagesAdmin)
admin.site.register(WeeklyProductionPlan)
admin.site.register(DailyPlan)
admin.site.register(ProductionPlanTotal)



@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'model')

@admin.register(DailyProductionPlan)
class DailyProductionPlanAdmin(admin.ModelAdmin):
    list_display = ('date', 's_no', 'get_unit_code', 'get_unit_model', 'qty_planned', 'qty_actual')

    def get_unit_code(self, obj):
        return obj.unit.code
    get_unit_code.short_description = 'Unit Code'

    def get_unit_model(self, obj):
        return obj.unit.model
    get_unit_model.short_description = 'Unit Model'

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

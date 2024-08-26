from django import forms
from .models import Screen, PDFFile, VideoFile

class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ['manager', 'product', 'upload_pdf', 'upload_video']
        widgets = {
            'upload_pdf': forms.CheckboxSelectMultiple(),
            'upload_video': forms.CheckboxSelectMultiple(),
        }

class PDFFileForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['pdf_duration', 'pdf_name', 'pdf_file']

class VideoFileForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['video_duration', 'video_name', 'video_file']


# ---------------------------------------------------------------

from django import forms
from .models import  DailyProductionPlan, Unit, ProductionPlan



class DailyProductionPlanForm(forms.ModelForm):
    class Meta:
        model = DailyProductionPlan
        fields = ['unit', 'assembly_line', 'qty_planned', 'qty_actual', 'remarks']
        widgets = {
            'unit': forms.Select(attrs={'class': 'select2'}),
            'assembly_line': forms.Select(attrs={'class': 'select2'}),
        }

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['date'].initial = self.instance.date
            
class ProductionPlanForm(forms.ModelForm):
    class Meta:
        model = ProductionPlan
        fields = ['unit', 'assembly_line', 'qty_planned', 'qty_actual', 'remarks']
        widgets = {
            'unit': forms.Select(attrs={'class': 'select2'}),
            'assembly_line': forms.Select(attrs={'class': 'select2'}),
        }

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['date'].initial = self.instance.date

       


class DailyProductionPlanForm2(forms.ModelForm):
    class Meta:
        model = DailyProductionPlan
        fields = ['unit', 'qty_planned', 'qty_actual', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.all()
        self.fields['unit'].widget.attrs.update({'onchange': 'updateUnitModel(this.value)'})



from .models import Images

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image_name', 'image_file', 'image_duration']
        widgets = {
            'image_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image_duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }




# from django import forms
# from .models import DailyProductionPlan, Unit, ProductionPlan
# from .form_models import WeeklyPlan, DailyPlan
# class WeeklyPlanForm(forms.ModelForm):
#     class Meta:
#         model = WeeklyPlan
#         fields = ['week_start_date', 'serial_number', 'remarks']
#         widgets = {
#             'week_start_date': forms.DateInput(attrs={'type': 'date'}),
#         }

# class DailyPlanForm(forms.ModelForm):
#     class Meta:
#         model = DailyPlan
#         fields = ['date', 'field1', 'unit']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#         }

# DailyPlanFormSet = forms.inlineformset_factory(
#     WeeklyPlan, DailyPlan, form=DailyPlanForm, extra=6, can_delete=True
# )






# --------------------------------------------------
from .form_models import WeeklyProductionPlan, DailyPlan
from django.forms.widgets import DateInput

class WeeklyProductionPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyProductionPlan
        fields = '__all__'

class DailyPlanForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=False
    )
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    weekly_plan = forms.ModelChoiceField(
        queryset=WeeklyProductionPlan.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'})
    )

    class Meta:
        model = DailyPlan
        fields = ['date', 'weekly_plan', 'quantity', 'unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['unit'].initial = self.instance.unit

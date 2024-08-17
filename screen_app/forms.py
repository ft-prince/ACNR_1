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
from .models import DailyProductionPlan,Unit

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

       

class DailyProductionPlanForm2(forms.ModelForm):
    class Meta:
        model = DailyProductionPlan
        fields = ['unit', 'qty_planned', 'qty_actual', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.all()
        self.fields['unit'].widget.attrs.update({'onchange': 'updateUnitModel(this.value)'})




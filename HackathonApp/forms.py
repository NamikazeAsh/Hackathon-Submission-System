from django.forms import DateInput
from django import forms

from HackathonApp.models import HackathonModel


typec =  (
    ('Image', 'Image'),
    ('File', 'File'),
    ('Link', 'Link'),
    )

class HackathonForm(forms.ModelForm):
    
    title = forms.CharField()
    description = forms.CharField(max_length=200)
    bgimg = forms.ImageField()
    hkimg = forms.ImageField()
    type = forms.ChoiceField(choices=typec)
    startdate = forms.DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ))
    enddate = forms.DateField(widget=DateInput(
        attrs={"type": "date", "class": "form-control"},
                format="%Y-%m-%d",
            ))
    reward = forms.IntegerField()
    
    class Meta:
        model = HackathonModel
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(HackathonForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['bgimg'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['hkimg'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['type'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['startdate'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['reward'].widget.attrs['class'] = 'form-control form-control-lg'

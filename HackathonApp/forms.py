from django.forms import DateInput
from django import forms

from HackathonApp.models import *


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
        
    
class SubmissionForm(forms.ModelForm):

    hackathonid = forms.ModelChoiceField(queryset=HackathonModel.objects.all())
    title = forms.CharField(max_length=100)
    summary = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500)
    coverimg = forms.ImageField()
    subimg = forms.ImageField()
    sublink = forms.URLField(max_length=200)
    subfile = forms.FileField()
    
    class Meta:
        model = SubmissionModel
        fields = "__all__"
        
        
    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['hackathonid'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['summary'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['coverimg'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['subimg'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['sublink'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['subfile'].widget.attrs['class'] = 'form-control form-control-lg'
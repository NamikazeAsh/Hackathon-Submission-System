from rest_framework import serializers
from django.forms import DateInput

from HackathonApp.models import *

typec =  (
    ('Image', 'Image'),
    ('File', 'File'),
    ('Link', 'Link'),
    )


class HackathonSerializer(serializers.ModelSerializer):

    title = serializers.CharField()
    description = serializers.CharField(max_length=200)
    bgimg = serializers.ImageField()
    hkimg = serializers.ImageField()
    type = serializers.ChoiceField(choices=typec)
    startdate = serializers.DateField()
    enddate = serializers.DateField()
    reward = serializers.IntegerField()
    
    class Meta:
        model = HackathonModel
        fields = '__all__'
        
        # def __init__(self, *args, **kwargs):
        #     super(HackathonSerializer, self).__init__(*args, **kwargs)
        #     self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['description'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['bgimg'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['hkimg'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['type'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['startdate'].widget.attrs['class'] = 'form-control form-control-lg'
        #     self.fields['reward'].widget.attrs['class'] = 'form-control form-control-lg'
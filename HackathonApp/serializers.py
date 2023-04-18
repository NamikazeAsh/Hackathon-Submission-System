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
        
class SubmissionSerializer(serializers.ModelSerializer):

    hackathonid = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=100)
    summary = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    coverimg = serializers.ImageField()
    subimg = serializers.ImageField()
    sublink = serializers.URLField(max_length=200)
    subfile = serializers.FileField()
    
    class Meta:
        
        model = SubmissionModel
        fields = ('hackathonid','username','title','summary','description','coverimg','subimg','sublink','subfile','type')
    
    
class UserModelSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField()
    userfavorites = SubmissionSerializer(many=True)
    
    class Meta:
        
        model = UserModel
        fields = "__all__"
        
from django.db import models

typec =  (
    ('Image', 'Image'),
    ('File', 'File'),
    ('Link', 'Link'),
    )

# Create your models here.
class HackathonModel(models.Model):
    
    title = models.TextField(max_length=100)
    description = models.TextField(max_length=200)
    bgimg = models.ImageField(upload_to = "images/bgimages")
    hkimg = models.ImageField(upload_to = "images/hkimages")
    type = models.CharField(max_length=100,choices=typec)
    startdate = models.DateField()
    enddate = models.DateField()
    reward = models.IntegerField()
    

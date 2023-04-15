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
    
class SubmissionModel(models.Model):

    hackathonid = models.ForeignKey(HackathonModel,on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    summary = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    coverimg = models.ImageField(upload_to = "images/coverimages")
    subimg = models.ImageField(null=True,blank=True,upload_to="images/subimages")
    sublink = models.URLField(max_length=200,null=True,blank=True)
    subfile = models.FileField(null=True,blank=True,upload_to="images/subfile")
    

from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

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
    
    def __str__(self):
        return f'{self.title}'
    
class SubmissionModel(models.Model):

    hackathonid = models.ForeignKey(HackathonModel,on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=100,null=True,blank=True)
    title = models.TextField(max_length=100)
    summary = models.TextField(max_length=100)
    description = models.TextField(max_length=500)
    coverimg = models.ImageField(upload_to = "images/coverimages")
    subimg = models.ImageField(null=True,blank=True,upload_to="images/subimages",validators=[FileExtensionValidator(['png','jpeg','jpg','ico',""])])
    sublink = models.URLField(null=True,blank=True,max_length=200,default="https://null.com")
    subfile = models.FileField(null=True,blank=True,upload_to="images/subfile",default="-",validators=[FileExtensionValidator(['pdf','csv','docx',""])])
    
    def __str__(self):
        return f'{self.title} for {self.hackathonid}'
    
class UserModel(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userfavorites = models.ManyToManyField(SubmissionModel,blank=True,related_name="userfavorites")
    usersubmissions = models.ManyToManyField(SubmissionModel,blank=True,related_name="usersubmissions")
    
    def __str__(self):
        return (str(self.user))

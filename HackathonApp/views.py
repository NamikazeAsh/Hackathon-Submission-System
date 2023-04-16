import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from HackathonApp.forms import *
from HackathonApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login

import mimetypes

def index(request):
    return render(request,"index.html")

def Dashboard(request):
    
    hackathons = HackathonModel.objects.all()
    context = {
        'hackathons' : hackathons
    }
    
    return render(request,"dashboard.html",context)

def SignUp(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username = username,email = email,password = password)
        user.save()
        
        return redirect('dashboard')
    
    return render(request,'signup.html')

def LogIn(request):
    
    if request.method == 'POST':
        
        if request.POST['username'] and request.POST['password']:
            
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            
            if authenticated_user is not None:
                login(request,authenticated_user)
        
        return redirect('dashboard')
        
    return render(request,"login.html")

def LogOut(request):
    
    if request.user:
        logout(request)
        
    return redirect('login')

def newHackathon(request):
    
    if request.method == 'POST':
        form = HackathonForm(request.POST,request.FILES)
        context = {'form':form}
        if form.is_valid():
            form.save()
            form = HackathonForm()
            return redirect('dashboard')
        else:
            print(form.errors)
            return redirect('dashboard')
    else:    
        form = HackathonForm()
        context = {'form':form,}
        return render(request,'newHackathon.html',context)
    
    
def HackathonDetail(request,id):
    
    hackathons = HackathonModel.objects.filter(id = id)
    submissions = SubmissionModel.objects.filter(hackathonid = id)
    print(submissions)
    
    return render(request,'hackathonDetail.html',{'hackathons':hackathons,'submissions':submissions})


def newSubmission(request,id):
    
    hackathon = HackathonModel.objects.get(id = id)

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST,request.FILES)
        context = {'form':form,'hackathon':hackathon}
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.hackathonid = hackathon
            form_data.type = hackathon.type
            form_data.save()
            
            form = SubmissionForm()
            print("--------- SAVED ----------")
            return redirect('dashboard')
            
        else:
            print(form.errors)
            
    else:    
        form = SubmissionForm()
        context = {
            'form':form,
            'hackathon' : hackathon
            }
        
    return render(request,'newSubmission.html',context)


def SubmissionDetail(request,id):

    submission = SubmissionModel.objects.get(id=id)
    
    return render(request,"submissionDetail.html",{'submission':submission})
        
        
def DownloadSubmission(request,id):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    submission = SubmissionModel.objects.get(id = id)

    if submission.type == "File":
        filename = submission.subfile.name
        filepath =  BASE_DIR + "/images/" + filename
        path = open(filepath, 'rb')
    elif submission.type == "Image":
        filename = submission.subimg.name
        filepath = BASE_DIR + '/images/' + filename
        path = open(filepath, 'rb')
    
    
    mime_type = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # os.remove("/tempfile/" + filename + " Solution") 
    
    return response
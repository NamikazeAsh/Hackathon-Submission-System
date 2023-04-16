import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from HackathonApp.forms import *
from HackathonApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

import mimetypes


def index(request):
    return render(request,"index.html")


@login_required(login_url='login')
def Dashboard(request):
    
    uid = request.user.id
    
    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    usermodelfav = []

    for a in usermodelf:
        usermodelfav.append(a[0])

    print("usermodelfav ",usermodelfav)

    favsubmissions = []
    if usermodelfav != []:    
        for x in usermodelfav:
            favsubmissions.append(SubmissionModel.objects.get(id = x))

    print(favsubmissions)
    hackathons = HackathonModel.objects.all()
    context = {
        'hackathons' : hackathons,
        'favsubmissions' : favsubmissions
    }
    
    return render(request,"dashboard.html",context)


def SignUp(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.create_user(username = username,email = email,password = password)
        user.save()
        
        um = UserModel.objects.create(user = user)
        um.save()
        
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


@login_required(login_url='login')
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
    
@login_required(login_url='login')
def HackathonDetail(request,id):
    
    hackathons = HackathonModel.objects.filter(id = id)
    submissions = SubmissionModel.objects.filter(hackathonid = id)
    print(submissions)
    
    return render(request,'hackathonDetail.html',{'hackathons':hackathons,'submissions':submissions})

@login_required(login_url='login')
def newSubmission(request,id):
    
    hackathon = HackathonModel.objects.get(id = id)

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST,request.FILES)
        context = {'form':form,'hackathon':hackathon}
        
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.hackathonid = hackathon
            form_data.type = hackathon.type
            curuser = str(request.user)
            print(curuser,type(curuser))
            form_data.username = curuser
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


@login_required(login_url='login')
def SubmissionDetail(request,id):

    submission = SubmissionModel.objects.get(id=id)
    uid = request.user.id

    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites')
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])
    print(usermodelfav)
    
    return render(request,"submissionDetail.html",{'submission':submission,'usermodelfav':usermodelfav})
        
        
@login_required(login_url='login')
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
    
    return response


@login_required(login_url='login')
def SubmissionsList(request):
    
    username = str(request.user)
    submissions = SubmissionModel.objects.filter(username = username)
    print(submissions)
    
    return render(request,"submissionList.html",{'submissions':submissions})


@login_required(login_url='login')
def SubmissionDelete(request,id):
    
    submissions = SubmissionModel.objects.get(id = id)
    submissions.delete()
    
    return redirect('dashboard')


@login_required(login_url='login')
def SubmissionEdit(request,id):
    
    submissionx = SubmissionModel.objects.get(id = id)
    hackathonid = submissionx.hackathonid
    htype = submissionx.type
    husername = submissionx.username
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST,instance=submissionx)
        if form.is_valid():
            
            form_data = form.save(commit=False)
            form_data.hackathonid = hackathonid
            form_data.type = htype
            form_data.username = husername
            form_data.save()
            
            form.save()
            
            return redirect('dashboard')
        else:
            print(form.errors)
    
    else:
        
        submissionx = SubmissionModel.objects.get(id = id)
        submission = submissionx 
            
        form = SubmissionForm(instance = submission)
        context = {'form':form}
    
    return render(request,'newSubmission.html',context)



@login_required(login_url='login')
def FavoriteSubmission(request,id):

    submission = SubmissionModel.objects.get(id=id)
    cuser = request.user
    uid = request.user.id

    usermodel = UserModel.objects.get(user=uid)
    usermodel.userfavorites.add(submission)
    
    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])
    print(usermodelfav)
    
    return SubmissionDetail(request,id)


@login_required(login_url='login')
def FavoriteSubmissionRemove(request,id):

    submission = SubmissionModel.objects.get(id=id)
    cuser = request.user
    uid = request.user.id

    usermodel = UserModel.objects.get(user=uid)
    usermodel.userfavorites.remove(submission)
    
    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])

    
    return SubmissionDetail(request,id)
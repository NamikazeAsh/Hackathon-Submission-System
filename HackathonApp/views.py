import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from HackathonApp.forms import *
from HackathonApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

import mimetypes


from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

def index(request):
    return render(request,"index.html")

@api_view(['GET'])
@login_required(login_url='login')
def Dashboard(request):
    
    uid = request.user.id
    
    i_usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    s_usermodelf = UserModelSerializer(data = i_usermodelf)
    usermodelf = s_usermodelf.initial_data
    
    usermodelfav = []

    for a in usermodelf:
        usermodelfav.append(a[0])

    favsubmissions = []
    if usermodelfav != [None]:    
        for x in usermodelfav:
            favsubmissions.append(SubmissionModel.objects.get(id = x))

    print(favsubmissions)
    
    hackathons = HackathonModel.objects.all()
    
    
    context = {
        'hackathons' : hackathons,
        'favsubmissions' : favsubmissions
    }
    
    return render(request,"dashboard.html",context)

@api_view(['POST','GET'])
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

@api_view(['POST','GET'])
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


@api_view(['POST','GET'])
@login_required(login_url='login')
def newHackathon(request):
    
    if request.method == 'POST':
        serializer = HackathonSerializer(data = request.data)

        if serializer.is_valid():
            print("valid serializer")
            serializer.save()
            return redirect('dashboard')
        else:
            print(serializer.errors)

    else:    
        return render(request,'newHackathon.html')
    
    
@api_view(['GET'])
@login_required(login_url='login')
def HackathonDetail(request,id):
    
    i_hackathons = HackathonModel.objects.filter(id = id)
    s_hackathons = HackathonSerializer(data = i_hackathons)
    hackathons = s_hackathons.initial_data
    
    i_submissions = SubmissionModel.objects.filter(hackathonid = id)
    s_submissions = SubmissionSerializer(data = i_submissions)
    submissions = s_submissions.initial_data
    
    print(submissions)
    
    return render(request,'hackathonDetail.html',{'hackathons':hackathons,'submissions':submissions})


@api_view(['POST','GET'])
@login_required(login_url='login')
def newSubmission(request,id):
    
    hackathon = HackathonModel.objects.get(id = id)

    if request.method == 'POST':
        
        form = SubmissionForm(request.POST,request.FILES)
        serializer = SubmissionSerializer(data = request.data)
        context = {'form':form,'hackathon':hackathon}
        
        if serializer.is_valid():
            serializer_data = serializer.save(commit = False)
            serializer_data.hackathonid = hackathon
            serializer_data.type = hackathon.type
            curuser = str(request.user)
            serializer_data.username = curuser
            serializer_data.save()
            
        else:
            print("ERRORS\n: ", serializer.errors)
            
    else:    
        context = {
            'hackathon' : hackathon
            }
        
    return render(request,'newSubmission.html',context)


@api_view(['GET'])
@login_required(login_url='login')
def SubmissionDetail(request,id):

    submission = SubmissionModel.objects.get(id=id)
    ssubmission = SubmissionSerializer(data = submission)
    uid = request.user.id

    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites')
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])
    # print(usermodelfav)
    
    return render(request,"submissionDetail.html",{'usermodelfav':usermodelfav,'ssubmission':ssubmission.initial_data})
        

@api_view(['POST','GET'])
@login_required(login_url='login')
def DownloadSubmission(request,id):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    i_submission = SubmissionModel.objects.get(id = id)
    s_submission = SubmissionSerializer(data = i_submission)
    submission = s_submission.initial_data

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


@api_view(['GET'])
@login_required(login_url='login')
def SubmissionsList(request):
    
    username = str(request.user)
    i_submissions = SubmissionModel.objects.filter(username = username)
    s_submissions = SubmissionSerializer(data = i_submissions)
    submissions = s_submissions.initial_data
    print(submissions)
    
    return render(request,"submissionList.html",{'submissions':submissions})

@api_view(['GET','DELETE'])
@login_required(login_url='login')
def SubmissionDelete(request,id):
    
    i_submissions = SubmissionModel.objects.get(id = id)
    s_submissions = SubmissionSerializer(data = i_submissions)
    submissions = s_submissions.initial_data
    submissions.delete()
    
    return redirect('dashboard')


@api_view(['GET','PUT','POST'])
@login_required(login_url='login')
def SubmissionEdit(request,id):
    
    i_submissionx = SubmissionModel.objects.get(id = id)
    s_submissionx = SubmissionSerializer(data = i_submissionx)
    submissionx = s_submissionx.initial_data
    
    hackathonid = submissionx.hackathonid.id
    htype = submissionx.type
    husername = submissionx.username
    
    if request.method == 'POST':

        form = SubmissionSerializer(data = submissionx)
        if form.is_valid():
            
            form_data = form.save(commit=False)
            form_data.hackathonid = hackathonid
            form_data.type = htype
            form_data.username = husername
            form_data.save()
            
            # form.save()
            
            return redirect('dashboard')
        else:
            print("---ERROR---\n",form.errors)
    
    else:
        i_submissionx = SubmissionModel.objects.get(id = id)
        s_submissionx = SubmissionSerializer(data = i_submissionx)
        submissionx = s_submissionx.initial_data
        
        i_hackathons = HackathonModel.objects.get(id = hackathonid)
        print("hackathonid ",hackathonid)
        s_hackathons = HackathonSerializer(data = i_hackathons)
        hackathon = s_hackathons.initial_data
        
        
        submission = submissionx 
        editing = True
        
        # form = SubmissionForm(instance = submission)
        # context = {'form':form}
    
    return render(request,'newSubmission.html',{'editing':editing,'submission':submission,'hackathon':hackathon})


@login_required(login_url='login')
def FavoriteSubmission(request,id):

    i_submission = SubmissionModel.objects.get(id=id)
    s_submission = SubmissionSerializer(data = i_submission)
    submission = s_submission.initial_data
    
    cuser = request.user
    uid = request.user.id

    i_usermodel = UserModel.objects.get(user=uid)
    s_usermodel = UserModelSerializer(data = i_usermodel)
    usermodel = s_usermodel.initial_data
    
    usermodel.userfavorites.add(submission)
    
    i_usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    s_usermodelf = UserModelSerializer(data= i_usermodelf)
    usermodelf = s_usermodelf.initial_data
    
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])
    print(usermodelfav)
    
    return SubmissionDetail(request,id)


@login_required(login_url='login')
def FavoriteSubmissionRemove(request,id):

    i_submission = SubmissionModel.objects.get(id=id)
    s_submission = SubmissionSerializer(data = i_submission)
    submission = s_submission.initial_data
    
    cuser = request.user
    uid = request.user.id

    i_usermodel = UserModel.objects.get(user=uid)
    s_usermodel = UserModelSerializer(data = i_usermodel)
    usermodel = s_usermodel.initial_data
    
    usermodel.userfavorites.remove(submission)
    
    usermodelf = UserModel.objects.filter(user = uid).values_list('userfavorites') 
    usermodelfav = []
    for a in usermodelf:
        usermodelfav.append(a[0])

    
    return SubmissionDetail(request,id)
from django.shortcuts import render,redirect
from HackathonApp.forms import *
from HackathonApp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login

def index(request):
    return render(request,"index.html")

def dashboard(request):
    
    hackathons = HackathonModel.objects.all()
    context = {
        'hackathons' : hackathons
    }
    print(request.user.username)
    
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
    
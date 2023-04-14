from django.shortcuts import render,redirect
from HackathonApp.forms import *
from HackathonApp.models import *

def index(request):
    return render(request,"index.html")

def dashboard(request):
    
    hackathons = HackathonModel.objects.all()
    context = {
        'hackathons' : hackathons
    }
    
    return render(request,"dashboard.html",context)

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,'signup.html')

def newHackathon(request):
    
    if request.method == 'POST':
        form = HackathonForm(request.POST,request.FILES)
        context = {'form':form}
        if form.is_valid():
            print("valid")
            form.save()
            form = HackathonForm()
            return redirect('dashboard')
        else:
            print("invalid form")
            print(form.errors)
            return redirect('dashboard')
    else:    
        form = HackathonForm()
        context = {'form':form,}
        return render(request,'newHackathon.html',context)
    
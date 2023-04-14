from django.shortcuts import render,redirect
from HackathonApp.forms import *

def index(request):
    return render(request,"index.html")

def dashboard(request):
    return render(request,"dashboard.html")

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
            return redirect('new-hackathon')
        else:
            print("invalid form")
            print(form.errors)
            return redirect('new-hackathon')
    else:    
        form = HackathonForm()
        context = {'form':form,}
        return render(request,'newHackathon.html',context)
    
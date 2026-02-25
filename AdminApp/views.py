from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from AdminApp.models import *



# Create your views here.
def dashboard(request):
    return render(request,'Dashboard.html')

def login(request):
    return render(request,'Login.html')

def add_student(request):
    return render(request,'Add_Student.html')
def admin_logout(request):
    return render(request,'Login.html')

def admin_login(request):
    uname=request.POST.get('username')
    pswd=request.POST.get('password')
    if User.objects.filter(username__contains=uname).exists():
        user=authenticate(username=uname,password=pswd)
        if user is not None:
            # login(request,user)
            request.session['username']=uname
            request.session['password']=pswd
            return redirect(dashboard)
        else:
            return redirect(login)
    else:
        return redirect(login)
def admin_logout(request):
    del request.session['username']
    del request.session['password'] 
    return redirect(login)

def manage_student(request):
    return render(request,'Manage_Student.html')
def add_class(request):
    return render(request,'Add_Class.html')
def manage_class(request):
    return render(request,'Manage_Class.html') 
def add_subject(request):
    return render(request,'Add_Subject.html')

def save_class(request):
    if request.method=='POST':
        Class_Name=request.POST.get('class_name')
        Section=request.POST.get('section')
        obj= ClassDb(Class_Name=Class_Name,Section=Section)
        obj.save()
        return redirect(save_class)        


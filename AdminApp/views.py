from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from AdminApp.models import *
from django.contrib import messages



# Create your views here.
def dashboard(request):
    return render(request,'Dashboard.html')

def login(request):
    return render(request,'Login.html')

def add_student(request):
    classes=ClassDb.objects.all()
    return render(request,'Add_Student.html',{'classes':classes})
def manage_subject(request):
    data=SubjectDb.objects.all()
    return render(request,'Manage_Subject.html',{'data':data})
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
# def manage_class(request):
#     return render(request,'Manage_Class.html') 
def add_subject(request):
    return render(request,'Add_Subject.html')

def save_class(request):
    if request.method=='POST':
        Class_Name=request.POST.get('class_name')
        Section=request.POST.get('section')
        obj= ClassDb(Class_Name=Class_Name,Section=Section)
        obj.save()
        messages.success(request,"Class Added Successfully")
        return redirect(add_class)        
def manage_class(request):
    data=ClassDb.objects.all()
    return render(request,'Manage_Class.html',{'data':data})
def delete_class(request,c_id):
    c=ClassDb.objects.get(id=c_id)
    c.delete()
    messages.success(request,"Class Deleted Successfully")
    return redirect(manage_class)
def edit_class(request,cl_id):
    data=ClassDb.objects.get(id=cl_id)
    return render(request,'Edit_Class.html',{'data':data})
def update_class(request,cl_id):
    if request.method=='POST':
        
        Class_Name=request.POST.get('class_name')
        Section=request.POST.get('section')
        c=ClassDb.objects.get(id=cl_id)  
        c.Class_Name=Class_Name
        c.Section=Section   
        c.save()
        messages.success(request,"Class Updated Successfully")
        return redirect(manage_class)   
def save_subject(request):
    if request.method=='POST':
        Subject_Name=request.POST.get('subject_name')
        Subject_Code=request.POST.get('subject_code')
        obj= SubjectDb(Subject_Name=Subject_Name,Subject_Code=Subject_Code)
        obj.save()
        messages.success(request,"Subject Added Successfully")
        return redirect(add_subject)  
def delete_subject(request,sub_id):
    s=SubjectDb.objects.get(id=sub_id)
    s.delete()
    messages.success(request,"Subject Deleted Successfully")
    return redirect(manage_subject)
def edit_subject(request,s_id):
    data=SubjectDb.objects.get(id=s_id)
    return render(request,'Edit_Subject.html',{'data':data})
def update_subject(request,s_id):
    if request.method=='POST':
        
        Subject_Name=request.POST.get('subject_name')
        Subject_Code=request.POST.get('subject_code')
        s=SubjectDb.objects.get(id=s_id)  
        s.Subject_Name=Subject_Name
        s.Subject_Code=Subject_Code   
        s.save()
        messages.success(request,"Subject Updated Successfully")
        return redirect(manage_subject)
    
   
    
        
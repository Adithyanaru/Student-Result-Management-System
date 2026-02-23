from django.shortcuts import render,redirect

# Create your views here.
def dashboard(request):
    return render(request,'Dashboard.html')

def add_student(request):
    return render(request,'Add_Student.html')
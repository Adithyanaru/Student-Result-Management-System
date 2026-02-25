from django.db import models

# Create your models here.
# class StudentDb(models.Model):
#     Name=models.CharField(max_length=100,null=True,blank=True)
#     Email=models.EmailField(max_length=100,null=True,blank=True)
#     Dob=models.DateField(null=True,blank=True)  
#     Id=models.In(max_length=100,null=True,blank=True)
#     Class=models.CharField(max_length=100,null=True,blank=True)
#     gender=models.CharField(max_length=100,null=True,blank=True)

class ClassDb(models.Model):
    Class_Name=models.CharField(max_length=100,null=True,blank=True)
    Section=models.CharField(max_length=100,null=True,blank=True)
    Created_At=models.DateTimeField(auto_now_add=True)
    Updated_At=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Class_Name
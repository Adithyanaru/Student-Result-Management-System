from django.db import models

class StudentDb(models.Model):
    Gender_Choices=(
        ('Male','Male'),
        ('Female','Female')
    )
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Dob=models.DateField(null=True,blank=True)  
    Class=models.ForeignKey('ClassDb', on_delete=models.CASCADE,null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,blank=True,choices=Gender_Choices)

class ClassDb(models.Model):
    Class_Name=models.CharField(max_length=100,null=True,blank=True)
    Section=models.CharField(max_length=100,null=True,blank=True)
    Created_At=models.DateTimeField(auto_now_add=True)
    Updated_At=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Class_Name

class SubjectDb(models.Model):
    Subject_Name=models.CharField(max_length=100,null=True,blank=True)
    Subject_Code=models.CharField(max_length=100,null=True,blank=True)
    Created_At=models.DateTimeField(auto_now_add=True)  
    Updated_At=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Subject_Name


class MarksDb(models.Model):
    Student=models.ForeignKey(StudentDb,on_delete=models.CASCADE,null=True,blank=True)
    Subject=models.ForeignKey(SubjectDb,on_delete=models.CASCADE,null=True,blank=True)
    Marks=models.IntegerField(null=True,blank=True)
    Created_At=models.DateTimeField(auto_now_add=True)  
    Updated_At=models.DateTimeField(auto_now=True)
    def __str__(self):   
             return f"{self.Student.Name} - {self.Subject.Subject_Name} - {self.Marks}"    
class ResultDb(models.Model):
    Student=models.ForeignKey(StudentDb,on_delete=models.CASCADE,null=True,blank=True)
    Total_Marks=models.IntegerField(null=True,blank=True)
    Percentage=models.FloatField(null=True,blank=True)
    Grade=models.CharField(max_length=100,null=True,blank=True)
    Created_At=models.DateTimeField(auto_now_add=True)  
    Updated_At=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.Student.Name} - {self.Total_Marks} - {self.Percentage} - {self.Grade}"   
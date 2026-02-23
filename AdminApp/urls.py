from django.urls import path
from AdminApp import views

urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_student/',views.add_student,name='add_student'),
]
from django.urls import path
from AdminApp import views

urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_student/',views.add_student,name='add_student'),
    path('login/',views.login,name='login'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('manage_student/',views.manage_student,name='manage_student'),
    path('add_class/',views.add_class,name='add_class'),
    path('manage_class/',views.manage_class,name='manage_class'),
    path('add_subject/',views.add_subject,name='add_subject'),


]
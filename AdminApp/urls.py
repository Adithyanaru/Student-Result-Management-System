from django.urls import path
from AdminApp import views

urlpatterns=[
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_student/',views.add_student,name='add_student'),
    path('login/',views.login,name='login'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('manage_student/',views.manage_student,name='manage_student'),

]
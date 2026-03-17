from WebApp import views
from django.urls import path
from django.contrib.auth.models import User


urlpatterns = [ 
    path('home/',views.home,name='home'),
    path('profile/', views.profile, name='profile'),
    path('st_login/',views.st_login,name='st_login'),
    path('student_login/',views.student_login,name='student_login'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('student_logout/',views.student_logout,name='student_logout'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('view_result/',views.view_result,name='view_result'),
    path('apply_arrear/',views.apply_arrear,name='apply_arrear'),
    path('save_arrear_payment/',views.save_arrear_payment,name='save_arrear_payment'),
    path('download_marksheet/',views.download_marksheet,name='download_marksheet'),
    
    path('notes/',views.notes,name='notes'),
   path('download-note/<int:id>/', views.download_note, name='download_note'),
]

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
    path('manage_subject/',views.manage_subject,name='manage_subject'),
    path('save_class/',views.save_class,name='save_class'),
    # path('manage_class/',views.manage_class,name='manage_class'),
    path('delete_class/<int:c_id>/',views.delete_class,name='delete_class'),
    path('edit_class/<int:cl_id>/',views.edit_class,name='edit_class'),
    path('update_class/<int:cl_id>/',views.update_class,name='update_class'),
    path('save_subject/',views.save_subject,name='save_subject'),
    path('delete_subject/<int:sub_id>/',views.delete_subject,name='delete_subject'),
    path('edit_subject/<int:s_id>/',views.edit_subject,name='edit_subject'),
    path('update_subject/<int:s_id>/',views.update_subject,name='update_subject'),
    path('save_student/',views.save_student,name='save_student'),
    path('manage_student/',views.manage_student,name='manage_student'),
    path('delete_student/<int:s_id>/',views.delete_student,name='delete_student'),
    path('edit_student/<int:st_id>/',views.edit_student,name='edit_student'),
    path('update_student/<int:st_id>/',views.update_student,name='update_student'),
    path('add_subject_combination/',views.add_subject_combination,name='add_subject_combination'),
    path('save_subject_combination/',views.save_subject_combination,name='save_subject_combination'),
    path('manage_subject_combination/',views.manage_subject_combination,name='manage_subject_combination'),
    path('delete_subject_combination/<int:sc_id>/',views.delete_subject_combination,name='delete_subject_combination'),
    path('add_notice/',views.add_notice,name='add_notice'), 
    path('save_notice/',views.save_notice,name='save_notice'),
    path('manage_notice/',views.manage_notice,name='manage_notice'),
    


]
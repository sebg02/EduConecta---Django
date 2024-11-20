from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('signin/', views.sign_in, name='sign_in'),
    path('home/', views.home, name='home'),
    path('logout/', views.log_out, name='log_out'),
    path('edit-teacher/', views.edit_profile_teacher, name='edit-teacher'),
    path('edit-student/', views.edit_profile_student, name='edit-student'),
    path('delete-user/', views.delete_user, name='delete-user'),
    path('create-class/', views.create_class, name='create-class'),
    path('delete-class/<int:class_id>', views.delete_class, name='delete-class'),
    path('edit-class/<int:class_id>', views.edit_class, name='edit-class'),
    path('filter-classes/', views.filter_classes, name='filter-classes'),
    path('send-enrollment-request/<int:class_id>', views.send_enrollment_request, name='send-enrollment-request'),
    path('handle-enrollment-request/', views.handle_enrollment_request, name='handle-enrollment-request'),
]
    
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
]
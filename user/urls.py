from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^login/', views.user_login, name='login'),
    re_path(r'^logout/', views.user_logout, name='logout'),
    re_path(r'^register/', views.user_register, name='register'),
    re_path(r'^facebook/', views.facebook, name='facebook'),
]

from django.shortcuts import render

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-credential/', views.add_credential, name='add_credential'),
    path('delete-credential/<int:pk>/', views.delete_credential, name='delete_credential'),
    path('add-group/', views.add_group, name='add_group'),
    path('delete-group/<int:pk>/', views.delete_group, name='delete_group'),
    path('add-post/', views.add_post, name='add_post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('load-data/', views.load_data, name='load_data'),
    path('run-automation/', views.run_automation_view, name='run_automation'),
]
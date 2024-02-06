from django.urls import path
from . import views

urlpatterns = [
    path('create_trial/', views.create_trial, name='create_trial'),
    path('create_round/', views.create_round, name='create_round'),
    path('create_calibration/', views.create_calibration, name='create_calibration'),
    path('create_form/', views.create_form, name='create_form'),
]

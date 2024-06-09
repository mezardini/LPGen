from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate, name='generate'),
    path('', views.index, name='index')
]

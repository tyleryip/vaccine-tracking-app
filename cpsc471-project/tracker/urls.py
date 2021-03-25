from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nurse_login/', views.nurse_login, name='nurse_login'),
    path('civilian_login/', views.civilian_login, name='civilian_login')
]